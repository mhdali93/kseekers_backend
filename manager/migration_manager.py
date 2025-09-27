#!/usr/bin/env python3

"""
Database Migration Manager for KSeekers Backend

This module provides a comprehensive migration system for managing database schema changes.
It supports both forward and backward migrations with proper versioning and rollback capabilities.
"""

import os
import sys
import logging
import time
from datetime import datetime
from typing import List, Dict, Optional, Tuple
from pathlib import Path

# Add project root to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import config
from manager.db_manager import get_db_connection, get_db_transaction

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)

class MigrationManager:
    """
    Manages database migrations with version control and rollback capabilities.
    """
    
    def __init__(self, migrations_dir: str = "migrations"):
        self.migrations_dir = Path(migrations_dir)
        self.migrations_dir.mkdir(exist_ok=True)
        self.migrations_table = "schema_migrations"
        
    def create_migrations_table(self):
        """Create the migrations tracking table if it doesn't exist."""
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(f"""
                CREATE TABLE IF NOT EXISTS {self.migrations_table} (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    version VARCHAR(50) NOT NULL UNIQUE,
                    name VARCHAR(255) NOT NULL,
                    applied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    checksum VARCHAR(64),
                    INDEX idx_version (version)
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
            """)
            conn.commit()
            logging.info(f"Created migrations table: {self.migrations_table}")
    
    def get_applied_migrations(self) -> List[str]:
        """Get list of applied migration versions."""
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(f"SELECT version FROM {self.migrations_table} ORDER BY version")
            return [row['version'] for row in cursor.fetchall()]
    
    def get_available_migrations(self) -> List[Tuple[str, str, str]]:
        """Get list of available migration files (version, name, filepath)."""
        migrations = []
        if not self.migrations_dir.exists():
            return migrations
            
        for file_path in sorted(self.migrations_dir.glob("*.sql")):
            filename = file_path.name
            if filename[0].isdigit() and "_" in filename:
                parts = filename.split("_", 1)
                if len(parts) == 2:
                    version = parts[0]
                    name = parts[1].replace(".sql", "").replace("_", " ")
                    migrations.append((version, name, str(file_path)))
        
        return migrations
    
    def get_pending_migrations(self) -> List[Tuple[str, str, str]]:
        """Get list of pending migrations that need to be applied."""
        applied = set(self.get_applied_migrations())
        available = self.get_available_migrations()
        return [migration for migration in available if migration[0] not in applied]
    
    def calculate_checksum(self, file_path: str) -> str:
        """Calculate MD5 checksum of a migration file."""
        import hashlib
        with open(file_path, 'rb') as f:
            return hashlib.md5(f.read()).hexdigest()
    
    def apply_migration(self, version: str, name: str, file_path: str) -> bool:
        """Apply a single migration."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                sql_content = f.read()
            
            if not sql_content.strip():
                logging.warning(f"Migration {version} is empty, skipping")
                return True
            
            checksum = self.calculate_checksum(file_path)
            
            with get_db_transaction() as conn:
                cursor = conn.cursor()
                
                # Execute the migration SQL
                logging.info(f"Applying migration {version}: {name}")
                for statement in sql_content.split(';'):
                    statement = statement.strip()
                    if statement:
                        cursor.execute(statement)
                
                # Record the migration
                cursor.execute(f"""
                    INSERT INTO {self.migrations_table} (version, name, checksum)
                    VALUES (%s, %s, %s)
                """, (version, name, checksum))
                
                conn.commit()
                logging.info(f"Successfully applied migration {version}: {name}")
                return True
                
        except Exception as e:
            logging.error(f"Failed to apply migration {version}: {e}")
            return False
    
    def rollback_migration(self, version: str) -> bool:
        """Rollback a single migration."""
        try:
            # Look for rollback file
            rollback_file = self.migrations_dir / f"R{version}.sql"
            if not rollback_file.exists():
                logging.error(f"Rollback file not found: {rollback_file}")
                return False
            
            with open(rollback_file, 'r', encoding='utf-8') as f:
                sql_content = f.read()
            
            if not sql_content.strip():
                logging.warning(f"Rollback migration {version} is empty")
                return True
            
            with get_db_transaction() as conn:
                cursor = conn.cursor()
                
                # Execute the rollback SQL
                logging.info(f"Rolling back migration {version}")
                for statement in sql_content.split(';'):
                    statement = statement.strip()
                    if statement:
                        cursor.execute(statement)
                
                # Remove the migration record
                cursor.execute(f"DELETE FROM {self.migrations_table} WHERE version = %s", (version,))
                
                conn.commit()
                logging.info(f"Successfully rolled back migration {version}")
                return True
                
        except Exception as e:
            logging.error(f"Failed to rollback migration {version}: {e}")
            return False
    
    def migrate_up(self, target_version: Optional[str] = None) -> bool:
        """Apply all pending migrations up to target version."""
        self.create_migrations_table()
        pending = self.get_pending_migrations()
        
        if not pending:
            logging.info("No pending migrations")
            return True
        
        if target_version:
            pending = [m for m in pending if m[0] <= target_version]
        
        success_count = 0
        for version, name, file_path in pending:
            if self.apply_migration(version, name, file_path):
                success_count += 1
            else:
                logging.error(f"Migration failed at version {version}")
                return False
        
        logging.info(f"Successfully applied {success_count} migrations")
        return True
    
    def migrate_down(self, target_version: Optional[str] = None) -> bool:
        """Rollback migrations down to target version."""
        self.create_migrations_table()
        applied = self.get_applied_migrations()
        
        if not applied:
            logging.info("No applied migrations to rollback")
            return True
        
        if target_version:
            applied = [v for v in applied if v > target_version]
        
        # Rollback in reverse order
        applied.reverse()
        
        success_count = 0
        for version in applied:
            if self.rollback_migration(version):
                success_count += 1
            else:
                logging.error(f"Rollback failed at version {version}")
                return False
        
        logging.info(f"Successfully rolled back {success_count} migrations")
        return True
    
    def status(self) -> Dict:
        """Get migration status information."""
        self.create_migrations_table()
        applied = self.get_applied_migrations()
        available = self.get_available_migrations()
        pending = self.get_pending_migrations()
        
        return {
            "applied_count": len(applied),
            "available_count": len(available),
            "pending_count": len(pending),
            "applied_migrations": applied,
            "pending_migrations": [(m[0], m[1]) for m in pending]
        }
    
    def create_migration(self, name: str) -> str:
        """Create a new migration file with sequential number."""
        # Get the next migration number
        available = self.get_available_migrations()
        if available:
            last_version = int(available[-1][0])
            version = f"{last_version + 1:02d}"
        else:
            version = "02"  # Start from 02 since 01 is initial schema
        
        # Create migration file
        migration_file = self.migrations_dir / f"{version}_{name}.sql"
        with open(migration_file, 'w', encoding='utf-8') as f:
            f.write(f"-- Migration: {name}\n")
            f.write(f"-- Version: {version}\n")
            f.write(f"-- Created: {datetime.now().isoformat()}\n\n")
            f.write("-- Add your SQL statements here\n")
        
        logging.info(f"Created migration file: {migration_file}")
        
        return version


def main():
    """Command line interface for migration manager."""
    import argparse
    
    parser = argparse.ArgumentParser(description="KSeekers Database Migration Manager")
    parser.add_argument("command", choices=["up", "down", "status", "create"], 
                       help="Migration command to execute")
    parser.add_argument("--target", help="Target version for up/down commands")
    parser.add_argument("--name", help="Name for create command")
    
    args = parser.parse_args()
    
    manager = MigrationManager()
    
    if args.command == "up":
        success = manager.migrate_up(args.target)
        sys.exit(0 if success else 1)
    
    elif args.command == "down":
        success = manager.migrate_down(args.target)
        sys.exit(0 if success else 1)
    
    elif args.command == "status":
        status = manager.status()
        print(f"Applied migrations: {status['applied_count']}")
        print(f"Available migrations: {status['available_count']}")
        print(f"Pending migrations: {status['pending_count']}")
        
        if status['pending_migrations']:
            print("\nPending migrations:")
            for version, name in status['pending_migrations']:
                print(f"  {version}: {name}")
    
    elif args.command == "create":
        if not args.name:
            print("Error: --name is required for create command")
            sys.exit(1)
        
        version = manager.create_migration(args.name)
        print(f"Created migration: {version}")


if __name__ == "__main__":
    main()
