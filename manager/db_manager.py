import traceback
import threading
import queue
import logging
import pymysql
import os
from contextlib import contextmanager
import config

class MySQLConnectionPool:
    """
    A custom MySQL connection pool implementation.
    
    This pool creates and maintains a specified number of database connections
    that can be reused across multiple operations, improving performance.
    """
    
    def __init__(self, host, port, user, password, database, max_connections=5):
        """Initialize the connection pool."""
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.database = database
        self.max_connections = max_connections
        self.pool = queue.Queue(maxsize=max_connections)
        self.size = 0
        self.lock = threading.Lock()
        
        # Pre-populate the pool with connections
        for _ in range(max_connections):
            self._add_connection()
        
        logging.info(f"MySQL connection pool initialized with {max_connections} connections to {host}:{port}/{database}")
    
    def _add_connection(self):
        """Add a new connection to the pool."""
        conn = pymysql.connect(
            host=self.host,
            port=self.port,
            user=self.user,
            password=self.password,
            database=self.database,
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor,
            autocommit=False
        )
        self.size += 1
        self.pool.put(conn)
    
    def get_connection(self):
        """Get a connection from the pool."""
        logging.info("Getting connection from pool")
        # Wait for an available connection
        conn = self.pool.get()
        return conn
    
    def release_connection(self, conn):
        """Return a connection to the pool."""
        logging.info("Releasing connection back to pool")
        # If the connection is still valid, put it back in the pool
        if conn:
            self.pool.put(conn)
    
    def close_all(self):
        """Close all connections in the pool."""
        logging.info("Closing all connections in the pool")
        with self.lock:
            while not self.pool.empty():
                try:
                    conn = self.pool.get(block=False)
                    if conn:
                        conn.close()
                        self.size -= 1
                except queue.Empty:
                    break


class DBManager:
    """
    Singleton database manager that provides MySQL connection pool for core SQL operations.
    """
    _instance = None
    __connection_pool__ = None
    
    def __new__(cls):
        try:
            if cls._instance is None:
                with threading.Lock() as dbmLock:
                    if cls._instance is None:
                        logging.info('Creating new DBManager instance')
                        cls._instance = super(DBManager, cls).__new__(cls)
            return cls._instance

        except Exception as ex:
            logging.error(f"Error while creating DBManager: {ex}")
            traceback.print_tb(ex.__traceback__)
            raise ex

    @staticmethod
    def get_instance():
        if DBManager._instance is None:
            logging.info("DBManager instance is None, creating new instance")
            with threading.Lock() as dbmLock:
                if DBManager._instance is None:
                    logging.info('Creating DBManager instance')
                    DBManager._instance = DBManager()

        return DBManager._instance
        
    def get_connection_pool(self):
        """Get or create the MySQL connection pool for direct SQL operations"""
        if self.__connection_pool__ is None:
            with threading.Lock() as dbmLock:
                if self.__connection_pool__ is None:
                    logging.info('Creating MySQL connection pool')
                    self.__connection_pool__ = MySQLConnectionPool(
                        host=config.db_host,
                        port=int(config.db_port),
                        user=config.db_user,
                        password=config.db_password,
                        database=config.mp_database,
                        max_connections=config.db_conn_pool
                    )
        return self.__connection_pool__
    
    def execute_query(self, query, params=None):
        """Execute a raw SQL query and return the results"""
        conn = None
        try:
            conn = self.get_connection_pool().get_connection()
            cursor = conn.cursor()
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            
            result = cursor.fetchall()
            return result
        except Exception as e:
            logging.error(f"Error executing query: {e}")
            raise e
        finally:
            if conn:
                self.get_connection_pool().release_connection(conn)
    
    def execute_update(self, query, params=None):
        """Execute a raw SQL update and return the number of affected rows"""
        conn = None
        try:
            conn = self.get_connection_pool().get_connection()
            cursor = conn.cursor()
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            
            conn.commit()
            return cursor.rowcount
        except Exception as e:
            if conn:
                conn.rollback()
            logging.error(f"Error executing update: {e}")
            raise e
        finally:
            if conn:
                self.get_connection_pool().release_connection(conn)
    
    def execute_insert(self, query, params=None):
        """Execute an INSERT query and return the last inserted ID"""
        conn = None
        try:
            conn = self.get_connection_pool().get_connection()
            cursor = conn.cursor()
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            
            conn.commit()
            return cursor.lastrowid
        except Exception as e:
            if conn:
                conn.rollback()
            logging.error(f"Error executing insert: {e}")
            raise e
        finally:
            if conn:
                self.get_connection_pool().release_connection(conn)
    
    def execute_many(self, query, params_list):
        """Execute a query multiple times with different parameters"""
        conn = None
        try:
            conn = self.get_connection_pool().get_connection()
            cursor = conn.cursor()
            cursor.executemany(query, params_list)
            conn.commit()
            return cursor.rowcount
        except Exception as e:
            if conn:
                conn.rollback()
            logging.error(f"Error executing many: {e}")
            raise e
        finally:
            if conn:
                self.get_connection_pool().release_connection(conn)


@contextmanager
def get_db_connection():
    """
    Context manager for database connections.
    Provides automatic connection management and error handling.
    """
    conn = None
    try:
        conn = DBManager.get_instance().get_connection_pool().get_connection()
        yield conn
    except Exception as e:
        if conn:
            conn.rollback()
        logging.error(f"Error in database connection: {e}")
        raise
    finally:
        if conn:
            DBManager.get_instance().get_connection_pool().release_connection(conn)


@contextmanager
def get_db_transaction():
    """
    Context manager for database transactions.
    Provides automatic transaction management with rollback on error.
    """
    conn = None
    try:
        conn = DBManager.get_instance().get_connection_pool().get_connection()
        yield conn
        conn.commit()
    except Exception as e:
        if conn:
            conn.rollback()
        logging.error(f"Error in database transaction: {e}")
        raise
    finally:
        if conn:
            DBManager.get_instance().get_connection_pool().release_connection(conn)
