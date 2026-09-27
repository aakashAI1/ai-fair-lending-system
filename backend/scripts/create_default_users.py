#!/usr/bin/env python3
"""
Create default users for authentication.
Run this script once to set up initial user accounts.
"""

import os
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.database import SessionLocal, init_db
from app.models import User
from app.api.routes.auth import get_password_hash

def create_default_users():
    """Create default user accounts."""
    password_env = {
        "EMP001": "ADMIN_USER_PASSWORD",
        "EMP002": "ANALYST_USER_PASSWORD",
        "EMP003": "MANAGER_USER_PASSWORD",
    }
    passwords = {employee_id: os.environ.get(variable) for employee_id, variable in password_env.items()}
    missing = [variable for employee_id, variable in password_env.items() if not passwords[employee_id]]
    if missing:
        raise RuntimeError("Set these environment variables before creating users: " + ", ".join(missing))

    init_db()
    db = SessionLocal()
    
    try:
        # Check if users already exist
        existing_users = db.query(User).count()
        if existing_users > 0:
            print(f"✅ Users already exist ({existing_users} users found)")
            print("Skipping user creation. Delete existing users if you want to recreate them.")
            return
        
        # Default users
        default_users = [
            {
                "employee_id": "EMP001",
                "password": passwords["EMP001"],
                "full_name": "Admin User",
                "email": "admin@fairlending.com",
                "role": "admin"
            },
            {
                "employee_id": "EMP002",
                "password": passwords["EMP002"],
                "full_name": "Analyst User",
                "email": "analyst@fairlending.com",
                "role": "analyst"
            },
            {
                "employee_id": "EMP003",
                "password": passwords["EMP003"],
                "full_name": "Manager User",
                "email": "manager@fairlending.com",
                "role": "manager"
            }
        ]
        
        print("=" * 70)
        print("CREATING DEFAULT USER ACCOUNTS")
        print("=" * 70)
        
        for user_data in default_users:
            user = User(
                employee_id=user_data["employee_id"],
                password_hash=get_password_hash(user_data["password"]),
                full_name=user_data["full_name"],
                email=user_data["email"],
                role=user_data["role"],
                is_active=True
            )
            db.add(user)
            print(f"✅ Created user: {user_data['employee_id']} ({user_data['role']})")
        
        db.commit()
        print("\n✅ SUCCESS! Default users created.")
        print("\nUser accounts created. Passwords were read from the environment and were not displayed.")
        for user_data in default_users:
            print(f"Employee ID: {user_data['employee_id']}")
            print(f"Role: {user_data['role']}")
            print("-" * 70)
        
    except Exception as e:
        db.rollback()
        print(f"❌ Error creating users: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    create_default_users()
