#!/usr/bin/env python3

"""
Migration Runner Script for KSeekers Backend

This script provides an easy way to run database migrations.
"""

import os
import sys
import argparse

# Add project root to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from manager.migration_manager import MigrationManager

def main():
    """Main function to run migrations"""
    parser = argparse.ArgumentParser(description="KSeekers Database Migration Runner")
    parser.add_argument("command", choices=["up", "down", "status", "create"], 
                       help="Migration command to execute")
    parser.add_argument("--target", help="Target version for up/down commands")
    parser.add_argument("--name", help="Name for create command")
    
    args = parser.parse_args()
    
    try:
        manager = MigrationManager()
        
        if args.command == "up":
            print("Running migrations up...")
            success = manager.migrate_up(args.target)
            if success:
                print("✅ Migrations completed successfully!")
            else:
                print("❌ Migration failed!")
                sys.exit(1)
        
        elif args.command == "down":
            print("Running migrations down...")
            success = manager.migrate_down(args.target)
            if success:
                print("✅ Rollback completed successfully!")
            else:
                print("❌ Rollback failed!")
                sys.exit(1)
        
        elif args.command == "status":
            print("Checking migration status...")
            status = manager.status()
            print(f"📊 Applied migrations: {status['applied_count']}")
            print(f"📊 Available migrations: {status['available_count']}")
            print(f"📊 Pending migrations: {status['pending_count']}")
            
            if status['pending_migrations']:
                print("\n⏳ Pending migrations:")
                for version, name in status['pending_migrations']:
                    print(f"  - {version}: {name}")
            else:
                print("\n✅ No pending migrations")
        
        elif args.command == "create":
            if not args.name:
                print("❌ Error: --name is required for create command")
                sys.exit(1)
            
            print(f"Creating migration: {args.name}")
            version = manager.create_migration(args.name)
            print(f"✅ Created migration: {version}")
    
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
