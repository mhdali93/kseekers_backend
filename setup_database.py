#!/usr/bin/env python3

"""
SQLite Database Setup Script for Scholar Dental
"""

import os
import sys
import sqlite3
import logging
import secrets
import time
from sqlmodel import SQLModel, create_engine
from datetime import datetime as dt

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

import config
from models.ormmodel import ResultDisplayConfig
from models.auth_models import User, OTP

def create_tables():
    """Create database tables using SQLModel ORM"""
    logging.info("Creating database tables...")
    
    # Create database directory if it doesn't exist
    db_dir = os.path.dirname(config.sqlite_db_path)
    if db_dir and not os.path.exists(db_dir):
        os.makedirs(db_dir)
    
    # Create engine and tables
    connection_string = f"sqlite:///{config.sqlite_db_path}"
    engine = create_engine(
        connection_string, 
        echo=config.db_echo,
        connect_args={"check_same_thread": False}
    )
    
    # Create all tables defined in SQLModel classes
    SQLModel.metadata.create_all(engine)
    
    # Ensure OTP table has the correct schema
    conn = sqlite3.connect(config.sqlite_db_path)
    cursor = conn.cursor()
    try:
        # Check if OTP table exists but has the old schema with purpose column
        cursor.execute("PRAGMA table_info(otps)")
        columns = cursor.fetchall()
        has_purpose = any(col[1] == 'purpose' for col in columns)
        
        if has_purpose:
            logging.info("Updating OTP table to remove purpose column...")
            # Create a new table without the purpose column
            cursor.execute("""
            CREATE TABLE otps_new (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                code TEXT NOT NULL,
                expires_at REAL NOT NULL,
                is_used INTEGER NOT NULL DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
            """)
            
            # Copy data from old table to new table
            cursor.execute("""
            INSERT INTO otps_new (id, user_id, code, expires_at, is_used, created_at)
            SELECT id, user_id, code, expires_at, is_used, created_at FROM otps
            """)
            
            # Drop old table and rename new table
            cursor.execute("DROP TABLE otps")
            cursor.execute("ALTER TABLE otps_new RENAME TO otps")
            
            conn.commit()
            logging.info("OTP table updated successfully")
    except Exception as e:
        conn.rollback()
        logging.error(f"Error updating OTP table: {e}")
    finally:
        conn.close()
    
    logging.info("Tables created successfully")

def create_lookup_tables():
    """Create lookup tables using raw SQL"""
    logging.info("Creating lookup tables...")
    
    # Connect to database
    conn = sqlite3.connect(config.sqlite_db_path)
    cursor = conn.cursor()
    
    try:
        # Create lookup_types table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS lookup_types (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            description TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)
        
        # Create lookup_values table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS lookup_values (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            lookup_type_id INTEGER NOT NULL,
            code TEXT NOT NULL,
            value TEXT NOT NULL,
            description TEXT,
            is_active INTEGER DEFAULT 1,
            sort_order INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (lookup_type_id) REFERENCES lookup_types(id)
        )
        """)
        
        # Create unique index
        cursor.execute("""
        CREATE UNIQUE INDEX IF NOT EXISTS idx_unique_lookup_code 
        ON lookup_values(lookup_type_id, code)
        """)
        
        conn.commit()
        logging.info("Lookup tables created successfully")
        
    except Exception as e:
        conn.rollback()
        logging.error(f"Error creating lookup tables: {e}")
        raise
    finally:
        conn.close()

def create_default_admin():
    """Create default admin user if none exists"""
    logging.info("Creating default admin user...")
    
    # Connect to database
    conn = sqlite3.connect(config.sqlite_db_path)
    cursor = conn.cursor()
    
    try:
        # Check if any users exist
        cursor.execute("SELECT COUNT(*) FROM users")
        count = cursor.fetchone()[0]
        
        if count == 0:
            # Create admin user
            now = dt.now()
            cursor.execute("""
            INSERT INTO users
            (username, email, phone, is_active, is_admin, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """, ('admin', 'admin@example.com', '1234567890', 1, 1, now, now))
            
            # Get admin ID
            admin_id = cursor.lastrowid
            
            # Create initial OTP
            code = f"{secrets.randbelow(1000000):06d}"
            expires_at = time.time() + 86400  # 24 hours
            
            cursor.execute("""
            INSERT INTO otps
            (user_id, code, expires_at, is_used, created_at)
            VALUES (?, ?, ?, ?, ?)
            """, (admin_id, code, expires_at, 0, now))
            
            conn.commit()
            
            logging.info("Default admin user created:")
            logging.info("Username: admin")
            logging.info("Email: admin@example.com")
            logging.info(f"Initial OTP: {code}")
        else:
            logging.info(f"Found {count} existing users - skipping admin creation")
            
    except Exception as e:
        conn.rollback()
        logging.error(f"Error creating admin user: {e}")
        raise
    finally:
        conn.close()

def main():
    """Main setup function"""
    logging.info("Starting database setup...")
    
    try:
        create_tables()
        create_lookup_tables()
        create_default_admin()
        
        logging.info(f"Setup complete! Database: {os.path.abspath(config.sqlite_db_path)}")
    except Exception as e:
        logging.error(f"Setup failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 