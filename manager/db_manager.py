import traceback
import threading
import queue
import logging
import sqlite3
import os
from urllib.parse import quote_plus

from sqlmodel import create_engine, Session
from sqlalchemy.pool import StaticPool
from sqlalchemy.exc import InvalidRequestError
import config

class SQLiteConnectionPool:
    """
    A custom SQLite connection pool implementation.
    
    This pool creates and maintains a specified number of database connections
    that can be reused across multiple operations, improving performance.
    """
    
    def __init__(self, db_file, max_connections=5):
        """Initialize the connection pool."""
        self.db_file = db_file
        self.max_connections = max_connections
        self.pool = queue.Queue(maxsize=max_connections)
        self.size = 0
        self.lock = threading.Lock()
        
        # Ensure the database directory exists
        db_dir = os.path.dirname(db_file)
        if db_dir and not os.path.exists(db_dir):
            os.makedirs(db_dir)
            
        # Pre-populate the pool with connections
        for _ in range(max_connections):
            self._add_connection()
        
        logging.info(f"SQLite connection pool initialized with {max_connections} connections to {db_file}")
    
    def _add_connection(self):
        """Add a new connection to the pool."""
        conn = sqlite3.connect(self.db_file)
        # Enable foreign keys
        conn.execute("PRAGMA foreign_keys = ON")
        # Configure connection to return rows as dictionaries
        conn.row_factory = sqlite3.Row
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
    Singleton database manager that provides SQLModel engine for ORM operations
    while using SQLite now and supporting MySQL in the future.
    """
    _instance = None
    __engine__ = None
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

    def get_engine(self):
        """Get SQLAlchemy engine for ORM operations"""
        if self.__engine__ is None:
            logging.info("DBEngine is None, creating new engine")

            try:
                with threading.Lock() as dbmLock:
                    if self.__engine__ is None:
                        logging.info('Creating DBEngine')
                        
                        # Use SQLite connection string
                        db_path = os.path.abspath(config.sqlite_db_path)
                        conn_string = f"sqlite:///{db_path}"
                        
                        logging.info(f"DB connection string: {conn_string}")
                        
                        # Create the engine with connection pooling
                        self.__engine__ = create_engine(
                            conn_string,
                            # SQLite-specific connection parameters
                            connect_args={"check_same_thread": False},
                            # Use StaticPool for in-memory SQLite
                            poolclass=StaticPool if db_path == ':memory:' else None,
                            # Echo SQL statements in debug mode
                            echo=config.db_echo
                        )

            except Exception as dex:
                logging.error(f"Error while creating DBEngine: {dex}")
                raise dex

        return self.__engine__
        
    def get_connection_pool(self):
        """Get or create the raw SQLite connection pool for direct SQL operations"""
        if self.__connection_pool__ is None:
            with threading.Lock() as dbmLock:
                if self.__connection_pool__ is None:
                    logging.info('Creating connection pool')
                    self.__connection_pool__ = SQLiteConnectionPool(
                        config.sqlite_db_path,
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


class DBSessionManager:
    """
    Context manager for SQLModel session management.
    Allows for easy transaction handling with the 'with' statement.
    """
    def __init__(self):
        self.__session = None
  
    def __enter__(self) -> Session:
        try:
            self.__session = Session(DBManager.get_instance().get_engine())
            return self.__session
        except Exception as ex:
            logging.error(f"Error in DBSessionManager: {ex}")
            raise
  
    def __exit__(self, ex_type, ex_mesg, ex_tb):
        logging.info(f"Exiting DBSessionManager - ex_type: {ex_type}")
        if ex_type:
            logging.error(f"Exception in DBSessionManager: {ex_mesg}")
            self.__session.rollback()
            traceback.print_tb(ex_tb)
        
        self.__session.close()
