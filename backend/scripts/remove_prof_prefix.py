"""
Script to remove PROF_ prefix from existing profile IDs in the database.
"""
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.database import SessionLocal
from app.models import StudentProfile
import re

def remove_prof_prefix():
    """Remove PROF_ prefix from all profile IDs."""
    db = SessionLocal()
    try:
        # Get all profiles with PROF_ prefix
        profiles = db.query(StudentProfile).filter(
            StudentProfile.profile_id.like('PROF_%')
        ).all()
        
        updated_count = 0
        for profile in profiles:
            old_id = profile.profile_id
            # Remove PROF_ prefix
            new_id = old_id.replace('PROF_', '').upper()
            
            # Check if new_id already exists (shouldn't happen, but safety check)
            existing = db.query(StudentProfile).filter(
                StudentProfile.profile_id == new_id
            ).first()
            
            if not existing:
                profile.profile_id = new_id
                updated_count += 1
                print(f"Updated: {old_id} -> {new_id}")
            else:
                print(f"Skipped {old_id} - {new_id} already exists")
        
        if updated_count > 0:
            db.commit()
            print(f"\n[SUCCESS] Successfully updated {updated_count} profile IDs!")
        else:
            print("\n[INFO] No profiles need updating.")
            
    except Exception as e:
        db.rollback()
        print(f"\n[ERROR] Error updating profiles: {e}")
        raise
    finally:
        db.close()

if __name__ == "__main__":
    print("Removing PROF_ prefix from profile IDs...")
    print("=" * 50)
    remove_prof_prefix()
    print("=" * 50)
    print("Done!")
