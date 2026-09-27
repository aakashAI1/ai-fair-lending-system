"""
Script to update all existing student profiles with realistic Indian names.
This replaces any fallback names like "Student STU_000000" with real names.
"""

import sys
import os
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

import random
from sqlalchemy.orm import Session

from app.database import SessionLocal, init_db
from app.models import StudentProfile

# Initialize database
init_db()

try:
    from app.data.indian_names import INDIAN_NAMES
except ImportError:
    # Fallback if module doesn't exist
    INDIAN_NAMES = [
        "Rajesh Kumar", "Priya Sharma", "Amit Patel", "Sneha Reddy", "Vikram Singh",
        "Anjali Gupta", "Rahul Mehta", "Kavita Desai", "Suresh Iyer", "Meera Nair",
        "Arjun Joshi", "Divya Rao", "Karan Malhotra", "Pooja Shah", "Nikhil Agarwal",
        "Riya Kapoor", "Aditya Verma", "Shreya Chaturvedi", "Rohan Bhatia", "Neha Trivedi",
        "Ravi Kumar", "Sunita Patel", "Manoj Singh", "Kiran Reddy", "Deepak Sharma",
        "Nisha Gupta", "Vivek Agarwal", "Manisha Desai", "Sachin Iyer", "Preeti Nair",
        "Akshay Kumar", "Jyoti Singh", "Varun Patel", "Swati Reddy", "Ajay Kumar",
        "Kavita Sharma", "Nikhil Patel", "Anita Iyer", "Rohit Nair", "Pooja Desai",
        "Siddharth Menon", "Ananya Krishnan", "Rohan Kapoor", "Isha Reddy", "Rahul Iyer",
        "Kritika Sharma", "Vishal Gupta", "Tanvi Patel", "Akash Kumar", "Sanjana Singh",
        "Harsh Malhotra", "Aishwarya Nair", "Karan Mehra", "Meera Joshi", "Rajat Verma",
        "Shreya Rao", "Arnav Agarwal", "Divya Chaturvedi", "Rohan Shah", "Neha Trivedi",
        "Ritvik Bhatia", "Akanksha Reddy", "Varun Iyer", "Kavya Sharma", "Sahil Patel",
        "Anushka Singh", "Pranav Kumar", "Dhruv Gupta", "Ishita Mehta", "Yash Desai",
        "Ria Kapoor", "Kabir Nair", "Aarav Joshi", "Zara Malhotra", "Veer Agarwal"
    ]


def update_profile_names():
    """Update all profiles with fallback names to have real Indian names."""
    db: Session = SessionLocal()
    try:
        # Get all profiles
        profiles = db.query(StudentProfile).all()
        
        updated_count = 0
        for profile in profiles:
            # Check if name is missing, empty, or is a fallback name
            name_str = str(profile.name).strip() if profile.name else ""
            is_fallback = (
                name_str.startswith("Student ") or 
                name_str == profile.profile_id or 
                not name_str or
                name_str.startswith("STU_")  # Also catch STU_ prefixed names
            )
            
            if is_fallback:
                old_name = profile.name
                profile.name = random.choice(INDIAN_NAMES)
                updated_count += 1
                print(f"Updated profile {profile.profile_id}: '{old_name}' -> '{profile.name}'")
        
        if updated_count > 0:
            db.commit()
            print(f"\n✅ Successfully updated {updated_count} profiles with real Indian names!")
        else:
            print("\n✅ All profiles already have real names. No updates needed.")
            
    except Exception as e:
        db.rollback()
        print(f"\n❌ Error updating profiles: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    print("Updating profile names with realistic Indian names...")
    update_profile_names()
