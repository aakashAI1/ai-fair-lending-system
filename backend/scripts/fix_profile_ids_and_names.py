"""
Script to update profile IDs to stud_XXX format and remove numbers from names.
"""
import sys
from pathlib import Path
import re

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.database import SessionLocal
from app.models import StudentProfile

def fix_profile_ids_and_names():
    """Update profile IDs to stud_XXX format and clean names."""
    db = SessionLocal()
    try:
        # Get all profiles ordered by ID
        profiles = db.query(StudentProfile).order_by(StudentProfile.id).all()
        
        updated_ids = 0
        updated_names = 0
        
        for idx, profile in enumerate(profiles, start=1):
            # Generate new profile ID in format stud_001, stud_002, etc.
            new_profile_id = f"stud_{idx:03d}"
            
            # Check if new ID already exists (shouldn't happen, but safety check)
            existing = db.query(StudentProfile).filter(
                StudentProfile.profile_id == new_profile_id
            ).first()
            
            if not existing:
                old_id = profile.profile_id
                profile.profile_id = new_profile_id
                updated_ids += 1
                if updated_ids <= 10:  # Print first 10 as examples
                    print(f"Updated ID: {old_id} -> {new_profile_id}")
            
            # Remove numbers from names (e.g., "Kiran Reddy 000" -> "Kiran Reddy")
            name_str = str(profile.name).strip()
            # Remove trailing numbers and spaces
            cleaned_name = re.sub(r'\s+\d+$', '', name_str).strip()
            
            if cleaned_name != name_str:
                profile.name = cleaned_name
                updated_names += 1
                if updated_names <= 10:  # Print first 10 as examples
                    print(f"Updated name: '{name_str}' -> '{cleaned_name}'")
        
        if updated_ids > 0 or updated_names > 0:
            db.commit()
            print(f"\n[SUCCESS] Updated {updated_ids} profile IDs and {updated_names} names!")
        else:
            print("\n[INFO] No profiles need updating.")
            
    except Exception as e:
        db.rollback()
        print(f"\n[ERROR] Error updating profiles: {e}")
        raise
    finally:
        db.close()

if __name__ == "__main__":
    print("Updating profile IDs to stud_XXX format and cleaning names...")
    print("=" * 60)
    fix_profile_ids_and_names()
    print("=" * 60)
    print("Done!")
