#!/usr/bin/env python3

"""
Database Setup Script for KSeekers

This script sets up the database by running migrations.
"""

import os
import sys
import logging
import mysql.connector
from mysql.connector import Error

# Add project root to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import config
from manager.migration_manager import MigrationManager

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)

def create_database_if_not_exists():
    """Create the database if it doesn't exist"""
    try:
        # Connect to MySQL server (without specifying database)
        conn = mysql.connector.connect(
            host=config.db_host,
            port=int(config.db_port),
            user=config.db_user,
            password=config.db_password,
            charset='utf8mb4'
        )
        
        cursor = conn.cursor()
        
        # Create database if it doesn't exist
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS `{config.ks_database}` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
        logging.info(f"Database '{config.ks_database}' is ready")
        
        # Close connection
        cursor.close()
        conn.close()
        
        return True
        
    except Exception as e:
        logging.error(f"Error creating database: {e}")
        return False

def main():
    """Main setup function"""
    logging.info("Setting up KSeekers database...")
    
    # Step 1: Create database if it doesn't exist
    logging.info("Step 1: Creating database if it doesn't exist...")
    if not create_database_if_not_exists():
        logging.error("Failed to create database")
        sys.exit(1)
    
    # Step 2: Run migrations
    logging.info("Step 2: Running database migrations...")
    try:
        manager = MigrationManager()
        success = manager.migrate_up()
        
        if success:
            logging.info("✅ Database setup completed successfully!")
        else:
            logging.error("❌ Migration failed!")
            sys.exit(1)
    
    except Exception as e:
        logging.error(f"Error running migrations: {e}")
        sys.exit(1)
    
    # Step 3: Show final status
    logging.info("Step 3: Checking final migration status...")
    try:
        manager = MigrationManager()
        status = manager.status()
        
        logging.info(f"📊 Applied migrations: {status['applied_count']}")
        logging.info(f"📊 Available migrations: {status['available_count']}")
        logging.info(f"📊 Pending migrations: {status['pending_count']}")
        
        if status['pending_count'] > 0:
            logging.warning("⚠️  There are still pending migrations!")
        else:
            logging.info("✅ All migrations are up to date!")
    
    except Exception as e:
        logging.error(f"Error checking status: {e}")
        sys.exit(1)
    
    logging.info("🎉 Database setup completed successfully!")

if __name__ == "__main__":
    main()