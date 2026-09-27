"""
Enhanced script to generate realistic, well-distributed student profiles
with proper bias patterns for accurate metrics calculation.
"""

import sys
import os
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

import random
import uuid
import numpy as np
from datetime import datetime
from sqlalchemy.orm import Session

from app.database import SessionLocal, init_db
from app.models import (
    StudentProfile, ScoringResult, BiasMetric, HumanFeedback, 
    MitigationResult, TestRun, TestDimension, ScoringType, SeverityLevel
)
from app.services.deterministic_scoring import DeterministicScoringEngine

# Initialize database
init_db()

# Sample data
INDIAN_NAMES = [
    "Rajesh Kumar", "Priya Sharma", "Amit Patel", "Sneha Reddy", "Vikram Singh",
    "Anjali Gupta", "Rahul Mehta", "Kavita Desai", "Suresh Iyer", "Meera Nair",
    "Arjun Joshi", "Divya Rao", "Karan Malhotra", "Pooja Shah", "Nikhil Agarwal",
    "Riya Kapoor", "Aditya Verma", "Shreya Chaturvedi", "Rohan Bhatia", "Neha Trivedi",
    "Ravi Kumar", "Sunita Patel", "Manoj Singh", "Kiran Reddy", "Deepak Sharma",
    "Nisha Gupta", "Vivek Agarwal", "Manisha Desai", "Sachin Iyer", "Preeti Nair"
]

STATES_URBAN = ["Delhi", "Mumbai", "Bangalore", "Chennai", "Kolkata", "Hyderabad", "Pune"]
STATES_RURAL_TIER2 = ["Bihar", "UP", "MP", "Odisha", "Rajasthan"]
STATES_RURAL_TIER3 = ["Jharkhand", "Chhattisgarh", "Assam", "Manipur", "Tripura"]

POSTCODES_URBAN = ["110001", "400001", "560001", "600001", "700001", "500001", "411001"]
POSTCODES_RURAL_TIER2 = ["841427", "201301", "486001", "751001", "302001"]
POSTCODES_RURAL_TIER3 = ["834001", "492001", "781001", "795001", "799001"]

COURSES = ["BTech", "BCom", "BSc", "MBA", "MCom", "BA", "BBA", "MCA", "BE", "BPharm"]
EDUCATIONAL_BACKGROUNDS = ["Engineering", "Commerce", "Science", "Arts"]
EMPLOYMENT_TYPES = ["salaried", "self-employed", "government", "student", "other"]
FAMILY_STRUCTURES = ["nuclear", "joint", "single_parent", "widow"]
CO_APPLICANTS = ["parent", "sibling", "spouse", "none"]

# Set seed for reproducibility
random.seed(42)
np.random.seed(42)


def generate_profile_realistic(profile_num: int, target_dimension: TestDimension = None) -> dict:
    """Generate a realistic student profile with proper distribution."""
    
    # Determine dimension if not specified
    if target_dimension is None:
        # Distribute across dimensions
        dims = list(TestDimension)
        target_dimension = dims[profile_num % len(dims)]
    
    # Geographic distribution
    # 40% urban_tier1, 35% rural_tier2, 25% rural_tier3
    geo_roll = profile_num % 100
    if geo_roll < 40:
        region = "urban_tier1"
        state = random.choice(STATES_URBAN)
        postcode = random.choice(POSTCODES_URBAN)
    elif geo_roll < 75:
        region = "rural_tier2"
        state = random.choice(STATES_RURAL_TIER2)
        postcode = random.choice(POSTCODES_RURAL_TIER2)
    else:
        region = "rural_tier3"
        state = random.choice(STATES_RURAL_TIER3)
        postcode = random.choice(POSTCODES_RURAL_TIER3)
    
    # Income distribution (normal distribution around 20L)
    if target_dimension == TestDimension.INCOME:
        # Force split for income dimension
        if profile_num % 2 == 0:
            # High income group
            family_income = int(np.random.normal(3500000, 500000))  # ~35L ± 5L
            family_income = max(2000000, min(5000000, family_income))
        else:
            # Low income group
            family_income = int(np.random.normal(1200000, 300000))  # ~12L ± 3L
            family_income = max(800000, min(1500000, family_income))
    else:
        # Normal distribution
        family_income = int(np.random.normal(2000000, 800000))  # ~20L ± 8L
        family_income = max(800000, min(5000000, family_income))
    
    # CIBIL score distribution (normal around 700)
    if target_dimension == TestDimension.CREDIT:
        # Force split for credit dimension
        credit_group = profile_num % 3
        if credit_group == 0:
            # Good credit (≥750)
            cibil_score = int(np.random.normal(800, 50))
            cibil_score = max(750, min(900, cibil_score))
        elif credit_group == 1:
            # Fair credit (650-750)
            cibil_score = int(np.random.normal(700, 40))
            cibil_score = max(650, min(749, cibil_score))
        else:
            # Poor credit (<600)
            cibil_score = int(np.random.normal(550, 50))
            cibil_score = max(300, min(599, cibil_score))
    else:
        # Normal distribution
        cibil_score = int(np.random.normal(700, 100))
        cibil_score = max(300, min(900, cibil_score))
    
    # GPA distribution (normal around 7.2 on Indian 10-point scale)
    gpa = round(np.random.normal(7.2, 1.0), 2)
    gpa = max(5.0, min(10.0, gpa))
    
    # Educational background distribution
    edu_roll = profile_num % 100
    if edu_roll < 40:
        educational_background = "Engineering"
        course = random.choice(["BTech", "BE", "BPharm"])
    elif edu_roll < 70:
        educational_background = "Commerce"
        course = random.choice(["BCom", "MBA", "MCom", "BBA"])
    elif edu_roll < 90:
        educational_background = "Science"
        course = random.choice(["BSc", "MCA"])
    else:
        educational_background = "Arts"
        course = random.choice(["BA"])
    
    # Employment type (weighted)
    emp_roll = profile_num % 100
    if emp_roll < 50:
        employment_type = "salaried"
    elif emp_roll < 70:
        employment_type = "self-employed"
    elif emp_roll < 85:
        employment_type = "government"
    elif emp_roll < 95:
        employment_type = "student"
    else:
        employment_type = "other"
    
    # Family structure (weighted)
    fam_roll = profile_num % 100
    if fam_roll < 60:
        family_structure = "nuclear"
    elif fam_roll < 85:
        family_structure = "joint"
    elif fam_roll < 95:
        family_structure = "single_parent"
    else:
        family_structure = "widow"
    
    # Co-applicant (weighted)
    co_app_roll = profile_num % 100
    if co_app_roll < 60:
        co_applicant = "parent"
    elif co_app_roll < 80:
        co_applicant = "sibling"
    elif co_app_roll < 90:
        co_applicant = "spouse"
    else:
        co_applicant = "none"
    
    # Loan amount (based on income, with some variation)
    base_loan = family_income * 0.5  # 50% of annual income
    loan_variation = base_loan * np.random.uniform(0.3, 0.7)
    requested_loan_amount = int(base_loan + loan_variation)
    requested_loan_amount = max(500000, min(5000000, requested_loan_amount))
    
    # Name (without numbers)
    name = random.choice(INDIAN_NAMES)
    
    # Determine test dimension
    if target_dimension == TestDimension.EDGE_CASES:
        # Force edge cases
        if profile_num % 4 == 0:
            employment_type = "self-employed"
        elif profile_num % 4 == 1:
            family_structure = "single_parent"
        elif profile_num % 4 == 2:
            family_structure = "widow"
        else:
            employment_type = "government"
    
    # Generate sequential profile ID: stud_001, stud_002, etc.
    # Note: This will be reassigned when saved to DB to ensure sequential numbering
    profile_id = f"stud_{profile_num % 1000:03d}"
    
    return {
        "profile_id": profile_id,
        "name": name,
        "postcode": postcode,
        "region": region,
        "state": state,
        "family_income": family_income,
        "cibil_score": cibil_score,
        "requested_loan_amount": requested_loan_amount,
        "gpa": gpa,
        "course": course,
        "educational_background": educational_background,
        "co_applicant": co_applicant,
        "employment_type": employment_type,
        "family_structure": family_structure,
        "test_dimension": target_dimension
    }


def populate_database_realistic(num_profiles: int = 500):
    """Populate database with realistic, well-distributed profiles."""
    db: Session = SessionLocal()
    scoring_engine = DeterministicScoringEngine()
    
    try:
        print("=" * 70)
        print("GENERATING REALISTIC STUDENT PROFILE DATA")
        print("=" * 70)
        
        print(f"\n[1/6] Clearing existing data...")
        db.query(MitigationResult).delete()
        db.query(HumanFeedback).delete()
        db.query(BiasMetric).delete()
        db.query(ScoringResult).delete()
        db.query(StudentProfile).delete()
        db.query(TestRun).delete()
        db.commit()
        
        print(f"[2/6] Creating test run...")
        test_run_id = f"TEST_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        test_run = TestRun(
            test_run_id=test_run_id,
            profile_count=num_profiles,
            dimensions_tested=[d.value for d in TestDimension],
            status="generating",
            progress_percentage=0.0
        )
        db.add(test_run)
        db.commit()
        
        print(f"[3/6] Generating {num_profiles} realistic student profiles...")
        profiles = []
        
        # Distribute profiles across dimensions
        profiles_per_dimension = num_profiles // len(TestDimension)
        
        for dim in TestDimension:
            print(f"  Generating {profiles_per_dimension} profiles for {dim.value} dimension...")
            for i in range(profiles_per_dimension):
                profile_data = generate_profile_realistic(len(profiles), dim)
                profile = StudentProfile(**profile_data)
                db.add(profile)
                profiles.append(profile)
        
        # Add any remaining profiles
        remaining = num_profiles - len(profiles)
        for i in range(remaining):
            profile_data = generate_profile_realistic(len(profiles))
            profile = StudentProfile(**profile_data)
            db.add(profile)
            profiles.append(profile)
        
        db.commit()
        print(f"[OK] Created {len(profiles)} profiles")
        
        print(f"[4/6] Scoring profiles (Fair and Biased models)...")
        scoring_count = 0
        
        for idx, profile in enumerate(profiles):
            profile_dict = {
                "profile_id": profile.profile_id,
                "name": profile.name,
                "postcode": profile.postcode,
                "region": profile.region,
                "state": profile.state,
                "family_income": profile.family_income,
                "cibil_score": profile.cibil_score,
                "requested_loan_amount": profile.requested_loan_amount,
                "gpa": profile.gpa,
                "course": profile.course,
                "educational_background": profile.educational_background,
                "co_applicant": profile.co_applicant,
                "employment_type": profile.employment_type,
                "family_structure": profile.family_structure,
                "test_dimension": profile.test_dimension.value
            }
            
            # Fair scoring
            fair_result = scoring_engine.calculate_fair_score(profile_dict)
            fair_scoring = ScoringResult(
                profile_id=profile.id,
                scoring_type=ScoringType.FAIR,
                score=fair_result["score"],
                approval_decision=fair_result["approval_decision"],
                interest_rate=fair_result["interest_rate"],
                collateral_required=fair_result["collateral_required"],
                reasoning=fair_result["reasoning"],
                prompt_version="fair_v1"
            )
            db.add(fair_scoring)
            
            # Biased scoring
            biased_result = scoring_engine.calculate_biased_score(profile_dict, fair_result)
            biased_scoring = ScoringResult(
                profile_id=profile.id,
                scoring_type=ScoringType.BIASED,
                score=biased_result["score"],
                approval_decision=biased_result["approval_decision"],
                interest_rate=biased_result["interest_rate"],
                collateral_required=biased_result["collateral_required"],
                reasoning=biased_result["reasoning"],
                prompt_version="biased_v1"
            )
            db.add(biased_scoring)
            
            scoring_count += 2
            
            if (idx + 1) % 50 == 0:
                db.commit()
                print(f"  Scored {idx + 1}/{len(profiles)} profiles...")
        
        db.commit()
        print(f"[OK] Created {scoring_count} scoring results")
        
        print(f"[5/6] Calculating bias metrics...")
        from app.services.metrics_service import MetricsService
        
        metrics_service = MetricsService(db)
        metrics_result = metrics_service.calculate_bias_metrics(
            test_run_id=test_run_id,
            dimensions=list(TestDimension)
        )
        
        metrics = db.query(BiasMetric).filter(
            BiasMetric.test_run_id == test_run_id
        ).all()
        
        print(f"[OK] Calculated {len(metrics)} bias metrics")
        
        # Update test run status
        test_run.status = "completed"
        test_run.progress_percentage = 100.0
        test_run.total_profiles_generated = len(profiles)
        test_run.total_profiles_scored = scoring_count
        test_run.total_metrics_calculated = len(metrics)
        test_run.completed_at = datetime.now()
        db.commit()
        
        print(f"[6/6] Generating sample human feedback...")
        
        # Create sample feedback for top findings
        if metrics:
            top_metric = max(metrics, key=lambda m: {
                "critical": 4, "high": 3, "medium": 2, "low": 1
            }.get(m.severity.value, 0))
            
            feedback = HumanFeedback(
                bias_metric_id=top_metric.id,
                is_discriminatory="yes",
                root_cause_analysis=(
                    f"The scoring model shows clear bias against {top_metric.group2_name} applicants. "
                    f"Approval parity of {top_metric.approval_parity:.2f} indicates systematic discrimination. "
                    f"This likely stems from unconscious bias in the scoring algorithm that overweights "
                    f"demographic and geographic factors rather than merit-based criteria."
                ),
                severity_rating=4 if top_metric.severity.value in ["high", "critical"] else 3,
                suggested_mitigation=(
                    "1. Remove geographic location from scoring criteria\n"
                    "2. Use income-adjusted metrics instead of absolute income\n"
                    "3. Add explicit fairness constraints in the scoring algorithm\n"
                    "4. Implement blind scoring for demographic factors"
                ),
                annotator_name="Dr. Priya Sharma",
                annotator_role="Senior Loan Officer"
            )
            db.add(feedback)
            db.commit()
            print(f"[OK] Created sample feedback")
        
        print("\n" + "=" * 70)
        print("DATA GENERATION COMPLETE!")
        print("=" * 70)
        print(f"\nSummary:")
        print(f"   - Test Run ID: {test_run_id}")
        print(f"   - Profiles Generated: {len(profiles)}")
        print(f"   - Scoring Results: {scoring_count}")
        print(f"   - Bias Metrics: {len(metrics)}")
        print(f"   - Human Feedback: {len(db.query(HumanFeedback).all())}")
        
        # Print metrics summary
        if metrics:
            print(f"\nBias Metrics Summary:")
            for metric in metrics[:5]:  # Show top 5
                print(f"   - {metric.dimension.value}: {metric.group1_name} vs {metric.group2_name}")
                print(f"     Approval Parity: {metric.approval_parity:.3f}, "
                      f"Fairness Score: {metric.overall_fairness_score:.1f}/100, "
                      f"Severity: {metric.severity.value}")
        
        print(f"\nAccess your application:")
        print(f"   - Dashboard: http://localhost:3000/dashboard")
        print(f"   - API Docs: http://localhost:8000/docs")
        print("=" * 70 + "\n")
        
    except Exception as e:
        db.rollback()
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    import sys
    import io
    
    # Fix encoding for Windows console
    if sys.platform == "win32":
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
        sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')
    
    # Number of profiles to generate (default 500 for good metrics)
    num_profiles = int(sys.argv[1]) if len(sys.argv) > 1 else 500
    print(f"Starting realistic data generation with {num_profiles} profiles...")
    populate_database_realistic(num_profiles)

