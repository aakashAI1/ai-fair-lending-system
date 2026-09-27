#!/usr/bin/env python3
"""
Import government student loan database (Prolog format) into our database.
Parses Prolog files and converts them to StudentProfile records.
"""

import re
import os
import sys
from pathlib import Path
from typing import Dict, List, Set, Optional
from collections import defaultdict
import random

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from sqlalchemy.orm import Session
from app.database import SessionLocal, init_db
from app.models import StudentProfile, TestDimension
from app.config import settings

# Data directory
DATA_DIR = Path(__file__).parent.parent.parent / "data_extracted"


def parse_prolog_file(filepath: Path) -> List[tuple]:
    """
    Parse a Prolog file and extract facts.
    Returns list of tuples (predicate_name, args...)
    """
    facts = []
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            for line in f:
                line = line.strip()
                # Skip comments and empty lines
                if not line or line.startswith('%'):
                    continue
                
                # Match Prolog facts: predicate(arg1, arg2, ...).
                match = re.match(r'(\w+)\((.*?)\)\.?$', line)
                if match:
                    predicate = match.group(1)
                    args_str = match.group(2)
                    
                    # Parse arguments (handle nested structures if needed)
                    args = []
                    current_arg = ""
                    depth = 0
                    
                    for char in args_str:
                        if char == '(':
                            depth += 1
                            current_arg += char
                        elif char == ')':
                            depth -= 1
                            current_arg += char
                        elif char == ',' and depth == 0:
                            args.append(current_arg.strip())
                            current_arg = ""
                        else:
                            current_arg += char
                    
                    if current_arg:
                        args.append(current_arg.strip())
                    
                    facts.append((predicate, tuple(args)))
    except Exception as e:
        print(f"Error parsing {filepath}: {e}")
    
    return facts


def load_all_data() -> Dict:
    """
    Load all Prolog data files and organize by student.
    """
    data = {
        'students': set(),
        'enrolled': {},  # student -> [(school, units), ...]
        'male': set(),
        'no_payment_due': set(),  # students with no payment due
        'longest_absence': {},  # student -> months
        'enlist': {},  # student -> [organizations, ...]
        'unemployed': set(),
        'filed_bankruptcy': set(),
        'disabled': set(),
    }
    
    # Parse each file
    files_to_parse = {
        'enrolled.pl': 'enrolled',
        'male.pl': 'male',
        'no_payment_due.pl': 'no_payment_due',
        'longest_absense_from_school.pl': 'longest_absence',
        'enlist.pl': 'enlist',
        'unemployed.pl': 'unemployed',
        'filed_for_bankrupcy.pl': 'filed_bankruptcy',
        'disabled.pl': 'disabled',
    }
    
    for filename, key in files_to_parse.items():
        filepath = DATA_DIR / filename
        if not filepath.exists():
            print(f"Warning: {filename} not found")
            continue
        
        print(f"Parsing {filename}...")
        facts = parse_prolog_file(filepath)
        
        for predicate, args in facts:
            if key == 'enrolled' and len(args) >= 3:
                student = args[0]
                school = args[1]
                units = args[2]
                if student not in data['enrolled']:
                    data['enrolled'][student] = []
                data['enrolled'][student].append((school, units))
                data['students'].add(student)
            
            elif key == 'male' and len(args) >= 1:
                student = args[0]
                data['male'].add(student)
                data['students'].add(student)
            
            elif key == 'no_payment_due' and len(args) >= 1:
                student = args[0]
                data['no_payment_due'].add(student)
                data['students'].add(student)
            
            elif key == 'longest_absence' and len(args) >= 2:
                student = args[0]
                months = args[1]
                try:
                    data['longest_absence'][student] = int(months)
                except ValueError:
                    pass
                data['students'].add(student)
            
            elif key == 'enlist' and len(args) >= 2:
                student = args[0]
                org = args[1]
                if student not in data['enlist']:
                    data['enlist'][student] = []
                data['enlist'][student].append(org)
                data['students'].add(student)
            
            elif key in ['unemployed', 'filed_bankruptcy', 'disabled'] and len(args) >= 1:
                student = args[0]
                data[key].add(student)
                data['students'].add(student)
    
    print(f"\nLoaded data for {len(data['students'])} students")
    print(f"  - Enrolled: {len(data['enrolled'])}")
    print(f"  - Male: {len(data['male'])}")
    print(f"  - No payment due: {len(data['no_payment_due'])}")
    print(f"  - Longest absence: {len(data['longest_absence'])}")
    print(f"  - Enlisted: {len(data['enlist'])}")
    print(f"  - Unemployed: {len(data['unemployed'])}")
    print(f"  - Filed bankruptcy: {len(data['filed_bankruptcy'])}")
    print(f"  - Disabled: {len(data['disabled'])}")
    
    return data


def map_to_student_profile(student_id: str, data: Dict) -> Optional[Dict]:
    """
    Map Prolog data to our StudentProfile schema.
    """
    # Extract student number
    student_num = int(re.search(r'\d+', student_id).group()) if re.search(r'\d+', student_id) else random.randint(1000, 9999)
    
    # Gender
    is_male = student_id in data['male']
    gender = "Male" if is_male else "Female"
    
    # Enrollment info
    enrollments = data['enrolled'].get(student_id, [])
    if not enrollments:
        return None  # Skip students with no enrollment data
    
    # Use first enrollment (or aggregate)
    school = enrollments[0][0] if enrollments else "unknown"
    total_units = sum(int(u) for _, u in enrollments)
    
    # Map schools to Indian context
    school_map = {
        'ucb': 'University of California, Berkeley',
        'ucsd': 'University of California, San Diego',
    }
    university = school_map.get(school, f"University {school}")
    
    # Absence
    absence_months = data['longest_absence'].get(student_id, 0)
    
    # Employment status
    is_unemployed = student_id in data['unemployed']
    employment_type = "student" if not is_unemployed else "unemployed"
    
    # Loan status (no_payment_due means they don't need to pay - could indicate special circumstances)
    no_payment_due = student_id in data['no_payment_due']
    
    # Generate realistic Indian student profile
    # Map to Indian context with realistic values
    regions = ["urban_tier1", "urban_tier2", "rural_tier2", "rural_tier3"]
    states = ["Maharashtra", "Karnataka", "Tamil Nadu", "Delhi", "Gujarat", "West Bengal"]
    
    # Use student number for consistent but varied data
    region_idx = student_num % len(regions)
    state_idx = student_num % len(states)
    
    # Income based on various factors
    base_income = 300000  # ₹3L base
    if no_payment_due:
        base_income += 200000  # Higher income if no payment due
    if is_unemployed:
        base_income -= 100000  # Lower if unemployed
    if student_id in data['disabled']:
        base_income -= 50000  # Lower if disabled
    
    income = base_income + (student_num % 500000)  # ₹3L to ₹8L
    
    # Credit score based on factors
    base_credit = 600
    if no_payment_due:
        base_credit += 50  # Better credit if no payment issues
    if student_id in data['filed_bankruptcy']:
        base_credit -= 150  # Much lower if bankruptcy
    if absence_months > 6:
        base_credit -= 30  # Lower if long absence
    
    credit_score = max(300, min(900, base_credit + (student_num % 200)))
    
    # GPA based on enrollment and absence (Indian 10-point scale)
    base_gpa = 7.0
    if total_units >= 3:
        base_gpa += 1.0
    if absence_months > 6:
        base_gpa -= 0.8
    if no_payment_due:
        base_gpa += 0.5
    
    gpa = max(5.0, min(10.0, base_gpa + (student_num % 100) / 50))
    
    # Course based on school
    courses = ["Engineering", "Medicine", "Business", "Arts", "Science", "Law"]
    course = courses[student_num % len(courses)]
    
    # Loan amount
    loan_amount = 1000000 + (student_num % 4000000)  # ₹10L to ₹50L
    
    # Determine test dimension based on data
    if is_male:
        test_dimension = TestDimension.GENDER
    elif region_idx >= 2:  # Rural
        test_dimension = TestDimension.GEOGRAPHIC
    elif income < 500000:
        test_dimension = TestDimension.INCOME
    elif credit_score < 600:
        test_dimension = TestDimension.CREDIT
    else:
        test_dimension = TestDimension.EDGE_CASES
    
    # Name
    names_male = ["Rajesh Kumar", "Amit Sharma", "Vikram Singh", "Rahul Patel", "Suresh Reddy"]
    names_female = ["Priya Sharma", "Anjali Patel", "Kavita Singh", "Meera Reddy", "Sneha Kumar"]
    name_list = names_male if is_male else names_female
    name = name_list[student_num % len(name_list)] + f" {student_num}"
    
    # Postcode (Indian format)
    postcode = f"{500000 + (student_num % 100000)}"
    
    # Family structure
    family_structures = ["nuclear", "joint", "single_parent"]
    family_structure = family_structures[student_num % len(family_structures)]
    
    # Co-applicant
    co_applicants = ["parent", "sibling", "spouse", "none"]
    co_applicant = co_applicants[student_num % len(co_applicants)]
    
    # Educational background
    edu_backgrounds = ["Graduate", "Post-Graduate", "Professional"]
    edu_background = edu_backgrounds[student_num % len(edu_backgrounds)]
    
    profile = {
        'profile_id': f"govt_{student_id}",
        'name': name,
        'postcode': postcode,
        'region': regions[region_idx],
        'state': states[state_idx],
        'family_income': income,
        'cibil_score': credit_score,
        'requested_loan_amount': loan_amount,
        'gpa': round(gpa, 2),
        'course': course,
        'educational_background': edu_background,
        'co_applicant': co_applicant,
        'employment_type': employment_type,
        'family_structure': family_structure,
        'test_dimension': test_dimension,
        # Additional metadata from government data
        '_metadata': {
            'original_id': student_id,
            'school': school,
            'total_units': total_units,
            'absence_months': absence_months,
            'no_payment_due': no_payment_due,
            'enlisted': student_id in data['enlist'],
            'disabled': student_id in data['disabled'],
            'filed_bankruptcy': student_id in data['filed_bankruptcy'],
        }
    }
    
    return profile


def import_data(db: Session, limit: Optional[int] = None):
    """
    Import government data into the database.
    """
    print("=" * 60)
    print("Importing Government Student Loan Database")
    print("=" * 60)
    
    # Load all data
    data = load_all_data()
    
    # Convert to profiles
    profiles = []
    students_list = sorted(data['students'])
    
    if limit:
        students_list = students_list[:limit]
    
    print(f"\nConverting {len(students_list)} students to profiles...")
    
    for student_id in students_list:
        profile_data = map_to_student_profile(student_id, data)
        if profile_data:
            profiles.append(profile_data)
    
    print(f"Created {len(profiles)} profiles")
    
    # Import to database
    print(f"\nImporting to database...")
    imported = 0
    skipped = 0
    
    for profile_data in profiles:
        # Check if already exists
        existing = db.query(StudentProfile).filter(
            StudentProfile.profile_id == profile_data['profile_id']
        ).first()
        
        if existing:
            skipped += 1
            continue
        
        # Create new profile
        profile = StudentProfile(**{k: v for k, v in profile_data.items() if k != '_metadata'})
        db.add(profile)
        imported += 1
        
        if imported % 100 == 0:
            print(f"  Imported {imported} profiles...")
            db.commit()
    
    db.commit()
    
    print(f"\n✅ Import complete!")
    print(f"  - Imported: {imported} new profiles")
    print(f"  - Skipped: {skipped} existing profiles")
    print(f"  - Total in database: {db.query(StudentProfile).count()}")


def main():
    """Main entry point."""
    # Initialize database
    init_db()
    
    # Create session
    db = SessionLocal()
    
    try:
        # Import all data (or limit for testing)
        import_limit = None  # Set to a number to limit imports for testing
        import_data(db, limit=import_limit)
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    main()

