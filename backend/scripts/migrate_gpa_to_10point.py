#!/usr/bin/env python3
"""
Migration script to convert existing GPA values from 4-point to 10-point scale.
Run this once after updating to 10-point GPA scale to update existing database records.
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from sqlalchemy.orm import Session
from app.database import SessionLocal, init_db
from app.models import StudentProfile
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize database
init_db()


def migrate_gpa_to_10point():
    """
    Convert all existing GPA values from 4-point scale to 10-point scale.
    Assumes any GPA <= 4.0 is on 4-point scale and needs conversion.
    """
    db: Session = SessionLocal()
    try:
        # Get all profiles with GPA <= 4.0 (likely 4-point scale)
        profiles = db.query(StudentProfile).filter(StudentProfile.gpa <= 4.0).all()
        
        if not profiles:
            logger.info("No profiles found with GPA <= 4.0. Migration not needed.")
            return
        
        logger.info(f"Found {len(profiles)} profiles with GPA <= 4.0. Converting to 10-point scale...")
        
        updated_count = 0
        for profile in profiles:
            old_gpa = profile.gpa
            # Convert 4-point to 10-point: multiply by 2.5
            new_gpa = old_gpa * 2.5
            # Ensure it's within valid range
            new_gpa = max(0.0, min(10.0, new_gpa))
            
            profile.gpa = new_gpa
            updated_count += 1
            
            if updated_count <= 5:  # Log first 5 as examples
                logger.info(f"  Profile {profile.profile_id}: {old_gpa:.2f} → {new_gpa:.2f}")
        
        # Commit all changes
        db.commit()
        logger.info(f"✅ Successfully migrated {updated_count} profiles to 10-point GPA scale!")
        logger.info(f"   All GPAs have been converted: 4-point value * 2.5 = 10-point value")
        
    except Exception as e:
        logger.error(f"Error during migration: {e}", exc_info=True)
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    logger.info("=" * 60)
    logger.info("GPA Migration: 4-point → 10-point scale")
    logger.info("=" * 60)
    logger.info("This will convert all GPAs <= 4.0 to 10-point scale.")
    logger.info("Conversion: new_gpa = old_gpa * 2.5")
    logger.info("")
    
    try:
        migrate_gpa_to_10point()
        logger.info("")
        logger.info("Migration completed successfully!")
    except Exception as e:
        logger.error(f"Migration failed: {e}")
        sys.exit(1)
