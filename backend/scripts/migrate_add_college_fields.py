#!/usr/bin/env python3
"""
Migration script to add college_tier and university_name columns to student_profiles table.
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
    """Add college_tier and university_name columns if they don't exist."""
    
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
        
        # Get current table structure
        cursor.execute("PRAGMA table_info(student_profiles)")
        columns = {row[1]: row for row in cursor.fetchall()}
        
        # Check and add college_tier column
        if 'college_tier' not in columns:
            logger.info("Adding college_tier column...")
            cursor.execute("ALTER TABLE student_profiles ADD COLUMN college_tier VARCHAR(50)")
            logger.info("✓ Added college_tier column")
        else:
            logger.info("✓ college_tier column already exists")
        
        # Check and add university_name column
        if 'university_name' not in columns:
            logger.info("Adding university_name column...")
            cursor.execute("ALTER TABLE student_profiles ADD COLUMN university_name VARCHAR(200)")
            logger.info("✓ Added university_name column")
        else:
            logger.info("✓ university_name column already exists")
        
        conn.commit()
        conn.close()
        
        logger.info("Migration completed successfully!")
        return True
        
    except Exception as e:
        logger.error(f"Migration failed: {e}", exc_info=True)
        return False


if __name__ == "__main__":
    logger.info("=" * 70)
    logger.info("DATABASE MIGRATION: Adding college_tier and university_name columns")
    logger.info("=" * 70)
    
    success = migrate_database()
    
    if success:
        logger.info("\nMigration completed. You can now run train_ml_model.py")
        sys.exit(0)
    else:
        logger.error("\nMigration failed. Please check the error messages above.")
        sys.exit(1)
