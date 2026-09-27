#!/usr/bin/env python3
"""
Migration script to add users table for authentication.
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

import sqlite3
from app.config import settings
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def migrate_database():
    """Create users table if it doesn't exist."""
    
    # Extract database file path from DATABASE_URL
    db_url = settings.DATABASE_URL
    if db_url.startswith("sqlite:///"):
        # sqlite:///./fairlending.db -> ./fairlending.db
        db_path = db_url.replace("sqlite:///", "")
        # Resolve relative path
        if db_path.startswith("./"):
            db_path = str(Path(__file__).parent.parent / db_path[2:])
        elif not db_path.startswith("/"):
            db_path = str(Path(__file__).parent.parent / db_path)
    else:
        logger.error(f"Unsupported database URL: {db_url}")
        return False
    
    logger.info(f"Connecting to database: {db_path}")
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Check if users table exists
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='users'")
        table_exists = cursor.fetchone() is not None
        
        if not table_exists:
            logger.info("Creating users table...")
            cursor.execute("""
                CREATE TABLE users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    employee_id VARCHAR(50) NOT NULL UNIQUE,
                    password_hash VARCHAR(255) NOT NULL,
                    full_name VARCHAR(200) NOT NULL,
                    email VARCHAR(200),
                    role VARCHAR(50) NOT NULL DEFAULT 'analyst',
                    is_active BOOLEAN NOT NULL DEFAULT 1,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    last_login DATETIME,
                    updated_at DATETIME
                )
            """)
            cursor.execute("CREATE INDEX ix_users_employee_id ON users(employee_id)")
            logger.info("✓ Created users table")
        else:
            logger.info("✓ users table already exists")
        
        conn.commit()
        conn.close()
        
        logger.info("Migration completed successfully!")
        return True
        
    except Exception as e:
        logger.error(f"Migration failed: {e}", exc_info=True)
        return False


if __name__ == "__main__":
    logger.info("=" * 70)
    logger.info("DATABASE MIGRATION: Creating users table for authentication")
    logger.info("=" * 70)
    
    success = migrate_database()
    
    if success:
        logger.info("\nMigration completed. You can now run create_default_users.py")
        sys.exit(0)
    else:
        logger.error("\nMigration failed. Please check the error messages above.")
        sys.exit(1)
