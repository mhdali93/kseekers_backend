#!/usr/bin/env python3

"""
Database Connection Pool Demo

This script demonstrates how to use the custom SQLite connection pool
implemented in the application. It shows both raw SQL queries and ORM operations.
"""

import os
import sys
import time
import random
import logging
import threading
from concurrent.futures import ThreadPoolExecutor
from sqlmodel import select, Session

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)

# Add project root to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import application modules
import config
from manager.db_manager import DBManager, DBSessionManager
from models.ormmodel import ResultDisplayConfig

def perform_direct_sql_query(query_type, iteration):
    """Perform a direct SQL query using the connection pool"""
    db_manager = DBManager.get_instance()
    
    try:
        # Build a query with a random condition for demonstration
        query = "SELECT * FROM result_display_config WHERE type = ? LIMIT 1"
        
        start_time = time.time()
        result = db_manager.execute_query(query, (query_type,))
        duration = time.time() - start_time
        
        thread_id = threading.get_ident()
        logging.info(f"SQL Query {iteration} (Thread {thread_id}): found {len(result)} results in {duration:.4f} seconds")
        
        return len(result)
    except Exception as e:
        logging.error(f"Error in SQL query {iteration}: {e}")
        return 0

def perform_orm_query(query_type, iteration):
    """Perform an ORM query using SQLModel and DBSessionManager"""
    try:
        start_time = time.time()
        
        with DBSessionManager() as session:
            query = select(ResultDisplayConfig).where(
                ResultDisplayConfig.type == query_type
            ).limit(1)
            
            result = session.exec(query).all()
        
        duration = time.time() - start_time
        
        thread_id = threading.get_ident()
        logging.info(f"ORM Query {iteration} (Thread {thread_id}): found {len(result)} results in {duration:.4f} seconds")
        
        return len(result)
    except Exception as e:
        logging.error(f"Error in ORM query {iteration}: {e}")
        return 0

def run_concurrent_queries(num_queries=20, query_types=None):
    """Run multiple queries concurrently to demonstrate connection pooling"""
    if query_types is None:
        query_types = ['string', 'date', 'number']
    
    logging.info(f"Running {num_queries} concurrent queries...")
    
    # Create a thread pool executor
    with ThreadPoolExecutor(max_workers=10) as executor:
        # Submit SQL and ORM queries
        sql_futures = [
            executor.submit(
                perform_direct_sql_query, 
                random.choice(query_types), 
                i
            ) 
            for i in range(num_queries // 2)
        ]
        
        orm_futures = [
            executor.submit(
                perform_orm_query, 
                random.choice(query_types), 
                i
            ) 
            for i in range(num_queries // 2)
        ]
        
        # Wait for all futures to complete
        all_futures = sql_futures + orm_futures
        for future in all_futures:
            future.result()
    
    logging.info("All queries completed")

def perform_write_operations(num_operations=5):
    """Demonstrate write operations using the connection pool"""
    db_manager = DBManager.get_instance()
    
    logging.info(f"Performing {num_operations} write operations...")
    
    for i in range(num_operations):
        try:
            # Example insert operation
            display_id = f"demo_id_{i}_{int(time.time())}"
            title = f"Demo Title {i}"
            key = f"demo_key_{i}"
            
            # First use direct SQL for insert
            query = """
            INSERT INTO result_display_config 
            (displayId, title, key, hidden, sorter, width, dataIndex, sortIndex, type, ellipsis)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """
            
            params = (
                display_id, title, key,
                0, 1, 100, key, 100 + i, 'demo', 0
            )
            
            start_time = time.time()
            db_manager.execute_update(query, params)
            duration = time.time() - start_time
            
            logging.info(f"SQL Insert {i}: completed in {duration:.4f} seconds")
            
            # Then use ORM for read and update
            with DBSessionManager() as session:
                # Read the record we just inserted
                stmt = select(ResultDisplayConfig).where(
                    ResultDisplayConfig.displayId == display_id
                )
                config = session.exec(stmt).first()
                
                if config:
                    # Update the record
                    config.title = f"Updated Title {i}"
                    session.add(config)
                    session.commit()
                    
                    logging.info(f"ORM Update {i}: updated record with ID {config.id}")
        
        except Exception as e:
            logging.error(f"Error in write operation {i}: {e}")

def main():
    """Main function to demonstrate the connection pool"""
    logging.info("=== SQLite Connection Pool Demo ===")
    
    # Make sure the database is properly set up
    if not os.path.exists(config.sqlite_db_path):
        logging.error(f"Database not found at {config.sqlite_db_path}")
        logging.info("Please run setup_database.py first to create the database")
        sys.exit(1)
    
    # Database manager stats
    db_manager = DBManager.get_instance()
    pool = db_manager.get_connection_pool()
    logging.info(f"Connection pool size: {pool.max_connections}")
    
    # Run concurrent queries to demonstrate connection pooling
    run_concurrent_queries(30)
    
    # Perform some write operations
    perform_write_operations()
    
    logging.info("Connection pool demo completed")

if __name__ == "__main__":
    main() 