"""
Script to populate database with realistic mock data for visualization.
This creates a complete dataset showing all features of the application.
"""

import sys
import os
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

import random
import uuid
from datetime import datetime, timedelta
from sqlalchemy.orm import Session

from app.database import SessionLocal, init_db
from app.models import (
    StudentProfile, ScoringResult, BiasMetric, HumanFeedback, 
    MitigationResult, TestRun, TestDimension, ScoringType, SeverityLevel
)

# Initialize database
init_db()

# Sample data
INDIAN_NAMES = [
    "Rajesh Kumar", "Priya Sharma", "Amit Patel", "Sneha Reddy", "Vikram Singh",
    "Anjali Gupta", "Rahul Mehta", "Kavita Desai", "Suresh Iyer", "Meera Nair",
    "Arjun Joshi", "Divya Rao", "Karan Malhotra", "Pooja Shah", "Nikhil Agarwal",
    "Riya Kapoor", "Aditya Verma", "Shreya Chaturvedi", "Rohan Bhatia", "Neha Trivedi"
]

# Research-based state distribution: 57% Southern, 16% Northern, 12% Western, 10% Eastern, 5% Northeastern
SOUTHERN_STATES = [
    {"state": "Maharashtra", "postcode": "400001", "region": "urban_tier1"},
    {"state": "Kerala", "postcode": "682001", "region": "urban_tier1"},
    {"state": "Andhra Pradesh", "postcode": "500001", "region": "urban_tier1"},
    {"state": "Tamil Nadu", "postcode": "600001", "region": "urban_tier1"},
    {"state": "Karnataka", "postcode": "560001", "region": "urban_tier1"},
    {"state": "Telangana", "postcode": "500001", "region": "urban_tier1"},
    {"state": "Tamil Nadu", "postcode": "625001", "region": "rural_tier2"},
    {"state": "Kerala", "postcode": "686001", "region": "rural_tier2"},
    {"state": "Karnataka", "postcode": "577001", "region": "rural_tier2"},
]

NORTHERN_STATES = [
    {"state": "Uttar Pradesh", "postcode": "201301", "region": "rural_tier2"},
    {"state": "Delhi", "postcode": "110001", "region": "urban_tier1"},
    {"state": "Punjab", "postcode": "141001", "region": "rural_tier2"},
    {"state": "Haryana", "postcode": "121001", "region": "rural_tier2"},
    {"state": "Uttarakhand", "postcode": "248001", "region": "rural_tier2"},
]

WESTERN_STATES = [
    {"state": "Gujarat", "postcode": "380001", "region": "urban_tier1"},
    {"state": "Rajasthan", "postcode": "302001", "region": "rural_tier2"},
    {"state": "Madhya Pradesh", "postcode": "486001", "region": "rural_tier2"},
]

EASTERN_STATES = [
    {"state": "West Bengal", "postcode": "700001", "region": "urban_tier1"},
    {"state": "Bihar", "postcode": "841427", "region": "rural_tier3"},
    {"state": "Odisha", "postcode": "751001", "region": "rural_tier3"},
    {"state": "Jharkhand", "postcode": "834001", "region": "rural_tier3"},
]

NORTHEASTERN_STATES = [
    {"state": "Assam", "postcode": "781001", "region": "rural_tier3"},
    {"state": "Tripura", "postcode": "799001", "region": "rural_tier3"},
    {"state": "Manipur", "postcode": "795001", "region": "rural_tier3"},
]

# Weighted state list: 57% Southern, 16% Northern, 12% Western, 10% Eastern, 5% Northeastern
ALL_STATES_WEIGHTED = list(
    SOUTHERN_STATES * 57 +
    NORTHERN_STATES * 16 +
    WESTERN_STATES * 12 +
    EASTERN_STATES * 10 +
    NORTHEASTERN_STATES * 5
)
# Shuffle for diversity while maintaining proportions
random.shuffle(ALL_STATES_WEIGHTED)

COURSES = ["BTech", "BCom", "BSc", "MBA", "MCom", "BA", "BBA", "MCA"]
EDUCATIONAL_BACKGROUNDS = ["Engineering", "Commerce", "Science", "Arts"]
EMPLOYMENT_TYPES = ["salaried", "self-employed", "government", "student", "other"]
FAMILY_STRUCTURES = ["nuclear", "joint", "single_parent", "widow"]
CO_APPLICANTS = ["parent", "sibling", "spouse", "none"]


def generate_profile(profile_num: int, dimension: TestDimension) -> dict:
    """Generate a realistic student profile with research-based state distribution."""
    # Use research-based weighted state distribution (57% Southern, etc.)
    state_info = ALL_STATES_WEIGHTED[profile_num % len(ALL_STATES_WEIGHTED)]
    state = state_info["state"]
    postcode = state_info["postcode"]
    region = state_info["region"]
    
    # Income distribution (more in middle range)
    if dimension == TestDimension.INCOME:
        if profile_num % 2 == 0:
            family_income = random.randint(2000000, 5000000)  # High income
        else:
            family_income = random.randint(800000, 1500000)  # Low income
    else:
        # Normal distribution around 20L
        base = 2000000
        family_income = int(base + random.gauss(0, 500000))
        family_income = max(800000, min(5000000, family_income))
    
    # CIBIL score (normal distribution around 650-750)
    if dimension == TestDimension.CREDIT:
        if profile_num % 3 == 0:
            cibil_score = random.randint(750, 900)  # Good credit
        elif profile_num % 3 == 1:
            cibil_score = random.randint(650, 750)  # Fair credit
        else:
            cibil_score = random.randint(300, 600)  # Poor credit
    else:
        cibil_score = int(random.gauss(700, 100))
        cibil_score = max(300, min(900, cibil_score))
    
    # GPA (normal distribution around 7.0 on Indian 10-point scale)
    gpa = round(random.gauss(7.0, 1.0), 2)
    gpa = max(5.0, min(10.0, gpa))
    
    # Edge cases
    if dimension == TestDimension.EDGE_CASES:
        employment_type = random.choice(["self-employed", "government", "student"])
        family_structure = random.choice(["single_parent", "widow", "nuclear"])
    else:
        employment_type = random.choice(EMPLOYMENT_TYPES)
        family_structure = random.choice(FAMILY_STRUCTURES)
    
    return {
        "profile_id": uuid.uuid4().hex[:8].upper(),
        "name": random.choice(INDIAN_NAMES),
        "postcode": postcode,
        "region": region,
        "state": state,
        "family_income": family_income,
        "cibil_score": cibil_score,
        "requested_loan_amount": random.randint(500000, 5000000),
        "gpa": gpa,
        "course": random.choice(COURSES),
        "educational_background": random.choice(EDUCATIONAL_BACKGROUNDS),
        "co_applicant": random.choice(CO_APPLICANTS),
        "employment_type": employment_type,
        "family_structure": family_structure,
        "test_dimension": dimension
    }


def calculate_fair_score(profile: dict) -> float:
    """Calculate fair score based on merit, credit, and capacity."""
    # Academic merit (40%)
    academic_score = (profile["gpa"] / 4.0) * 4.0
    
    # Creditworthiness (30%)
    credit_score = ((profile["cibil_score"] - 300) / 600) * 3.0
    
    # Repayment capacity (30%)
    income_ratio = profile["family_income"] / profile["requested_loan_amount"]
    capacity_score = min(3.0, (income_ratio / 2.0) * 3.0)
    
    base_score = academic_score + credit_score + capacity_score
    
    # Add some randomness
    score = base_score + random.gauss(0, 0.5)
    return max(1.0, min(10.0, round(score, 2)))


def calculate_biased_score(profile: dict, fair_score: float) -> float:
    """Calculate biased score by applying penalties."""
    score = fair_score
    
    # Rural penalty
    if "rural" in profile["region"]:
        score -= 2.0
    
    # Low income penalty
    if profile["family_income"] < 2000000:
        score -= 1.0
    
    # Self-employed penalty
    if profile["employment_type"] == "self-employed":
        score -= 1.5
    
    # Tier-2/3 penalty
    if "tier2" in profile["region"] or "tier3" in profile["region"]:
        score -= 1.0
    
    # State-based penalty
    if profile["state"] in ["Bihar", "UP", "MP"]:
        score -= 0.5
    
    return max(1.0, min(10.0, round(score, 2)))


def get_approval_decision(score: float) -> str:
    """Determine approval decision based on score."""
    if score >= 9.0:
        return "approve"
    elif score >= 7.0:
        return "approve"
    elif score >= 5.0:
        return "conditional"
    else:
        return "reject"


def get_interest_rate(score: float) -> float:
    """Determine interest rate based on score."""
    if score >= 9.0:
        return 9.0
    elif score >= 7.0:
        return 11.0
    elif score >= 5.0:
        return 13.0
    else:
        return 15.0


def get_collateral_required(score: float) -> bool:
    """Determine if collateral is required."""
    return score < 7.0


def populate_database():
    """Populate database with mock data."""
    db: Session = SessionLocal()
    
    try:
        print("[1/6] Clearing existing data...")
        print("   (Removing old profiles with outdated state distribution...)")
        db.query(MitigationResult).delete()
        db.query(HumanFeedback).delete()
        db.query(BiasMetric).delete()
        db.query(ScoringResult).delete()
        db.query(StudentProfile).delete()
        db.query(TestRun).delete()
        db.commit()
        print("   ✅ Cleared all existing data")
        print("   ✅ Using research-based state distribution (57% Southern states)")
        
        print("[2/6] Creating test run...")
        test_run_id = f"TEST_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        test_run = TestRun(
            test_run_id=test_run_id,
            profile_count=100,
            dimensions_tested=[d.value for d in TestDimension],
            status="completed",
            progress_percentage=100.0,
            total_profiles_generated=100,
            total_profiles_scored=100,
            total_metrics_calculated=8,
            completed_at=datetime.now()
        )
        db.add(test_run)
        db.commit()
        
        print("[3/6] Generating 100 student profiles...")
        profiles = []
        for i in range(100):
            dimension = random.choice(list(TestDimension))
            profile_data = generate_profile(i, dimension)
            profile = StudentProfile(**profile_data)
            db.add(profile)
            profiles.append(profile)
        db.commit()
        print(f"[OK] Created {len(profiles)} profiles")
        
        print("[4/6] Generating scoring results (fair and biased)...")
        scoring_count = 0
        for profile in profiles:
            # Fair scoring
            fair_score = calculate_fair_score({
                "gpa": profile.gpa,
                "cibil_score": profile.cibil_score,
                "family_income": profile.family_income,
                "requested_loan_amount": profile.requested_loan_amount
            })
            
            fair_result = ScoringResult(
                profile_id=profile.id,
                scoring_type=ScoringType.FAIR,
                score=fair_score,
                approval_decision=get_approval_decision(fair_score),
                interest_rate=get_interest_rate(fair_score),
                collateral_required=get_collateral_required(fair_score),
                reasoning=f"Fair scoring based on academic merit ({profile.gpa} GPA), creditworthiness ({profile.cibil_score} CIBIL), and repayment capacity.",
                prompt_version="fair_v1"
            )
            db.add(fair_result)
            
            # Biased scoring
            biased_score = calculate_biased_score({
                "region": profile.region,
                "family_income": profile.family_income,
                "employment_type": profile.employment_type,
                "state": profile.state
            }, fair_score)
            
            biased_result = ScoringResult(
                profile_id=profile.id,
                scoring_type=ScoringType.BIASED,
                score=biased_score,
                approval_decision=get_approval_decision(biased_score),
                interest_rate=get_interest_rate(biased_score),
                collateral_required=get_collateral_required(biased_score),
                reasoning=f"Scoring considers regional risk factors and income stability. {profile.region} location and {profile.employment_type} employment type influence assessment.",
                prompt_version="biased_v1"
            )
            db.add(biased_result)
            scoring_count += 2
        
        db.commit()
        print(f"[OK] Created {scoring_count} scoring results")
        
        print("[5/6] Calculating bias metrics...")
        
        # Get all profiles with scores
        all_profiles = db.query(StudentProfile).all()
        fair_scores = {s.profile_id: s for s in db.query(ScoringResult).filter(ScoringResult.scoring_type == ScoringType.FAIR).all()}
        biased_scores = {s.profile_id: s for s in db.query(ScoringResult).filter(ScoringResult.scoring_type == ScoringType.BIASED).all()}
        
        # Geographic metrics: Urban vs Rural
        urban_profiles = [p for p in all_profiles if "urban" in p.region]
        rural_profiles = [p for p in all_profiles if "rural" in p.region]
        
        if urban_profiles and rural_profiles:
            urban_approvals = sum(1 for p in urban_profiles if biased_scores[p.id].approval_decision == "approve")
            rural_approvals = sum(1 for p in rural_profiles if biased_scores[p.id].approval_decision == "approve")
            urban_approval_rate = urban_approvals / len(urban_profiles)
            rural_approval_rate = rural_approvals / len(rural_profiles) if rural_profiles else 0
            approval_parity = urban_approval_rate / rural_approval_rate if rural_approval_rate > 0 else 0
            
            urban_interest = sum(biased_scores[p.id].interest_rate for p in urban_profiles) / len(urban_profiles)
            rural_interest = sum(biased_scores[p.id].interest_rate for p in rural_profiles) / len(rural_profiles)
            interest_gap = abs(urban_interest - rural_interest)
            
            urban_collateral = sum(1 for p in urban_profiles if biased_scores[p.id].collateral_required) / len(urban_profiles) * 100
            rural_collateral = sum(1 for p in rural_profiles if biased_scores[p.id].collateral_required) / len(rural_profiles) * 100
            collateral_gap = abs(urban_collateral - rural_collateral)
            
            fairness_score = 75.0  # Simplified calculation
            severity = SeverityLevel.MEDIUM if approval_parity < 0.95 else SeverityLevel.LOW
            
            metric = BiasMetric(
                test_run_id=test_run_id,
                dimension=TestDimension.GEOGRAPHIC,
                approval_parity=round(approval_parity, 3),
                interest_rate_disparity=round(interest_gap, 2),
                collateral_gap=round(collateral_gap, 2),
                edge_case_coverage=95.0,
                overall_fairness_score=round(fairness_score, 2),
                p_value=0.023,
                t_statistic=2.45,
                is_statistically_significant=True,
                confidence_interval_lower=-0.15,
                confidence_interval_upper=-0.05,
                severity=severity,
                group1_name="Urban",
                group2_name="Rural",
                group1_approval_rate=round(urban_approval_rate, 3),
                group2_approval_rate=round(rural_approval_rate, 3),
                group1_interest_rate=round(urban_interest, 2),
                group2_interest_rate=round(rural_interest, 2),
                group1_collateral_pct=round(urban_collateral, 2),
                group2_collateral_pct=round(rural_collateral, 2)
            )
            db.add(metric)
        
        # Income metrics: High vs Low
        high_income_profiles = [p for p in all_profiles if p.family_income >= 2000000]
        low_income_profiles = [p for p in all_profiles if p.family_income < 1500000]
        
        if high_income_profiles and low_income_profiles:
            high_approvals = sum(1 for p in high_income_profiles if biased_scores[p.id].approval_decision == "approve")
            low_approvals = sum(1 for p in low_income_profiles if biased_scores[p.id].approval_decision == "approve")
            high_approval_rate = high_approvals / len(high_income_profiles)
            low_approval_rate = low_approvals / len(low_income_profiles) if low_income_profiles else 0
            approval_parity = high_approval_rate / low_approval_rate if low_approval_rate > 0 else 0
            
            high_interest = sum(biased_scores[p.id].interest_rate for p in high_income_profiles) / len(high_income_profiles)
            low_interest = sum(biased_scores[p.id].interest_rate for p in low_income_profiles) / len(low_income_profiles)
            interest_gap = abs(high_interest - low_interest)
            
            high_collateral = sum(1 for p in high_income_profiles if biased_scores[p.id].collateral_required) / len(high_income_profiles) * 100
            low_collateral = sum(1 for p in low_income_profiles if biased_scores[p.id].collateral_required) / len(low_income_profiles) * 100
            collateral_gap = abs(high_collateral - low_collateral)
            
            fairness_score = 72.0
            severity = SeverityLevel.HIGH if approval_parity < 0.85 else SeverityLevel.MEDIUM
            
            metric = BiasMetric(
                test_run_id=test_run_id,
                dimension=TestDimension.INCOME,
                approval_parity=round(approval_parity, 3),
                interest_rate_disparity=round(interest_gap, 2),
                collateral_gap=round(collateral_gap, 2),
                edge_case_coverage=95.0,
                overall_fairness_score=round(fairness_score, 2),
                p_value=0.015,
                t_statistic=2.78,
                is_statistically_significant=True,
                confidence_interval_lower=-0.20,
                confidence_interval_upper=-0.08,
                severity=severity,
                group1_name="High Income (≥₹20L)",
                group2_name="Low Income (<₹15L)",
                group1_approval_rate=round(high_approval_rate, 3),
                group2_approval_rate=round(low_approval_rate, 3),
                group1_interest_rate=round(high_interest, 2),
                group2_interest_rate=round(low_interest, 2),
                group1_collateral_pct=round(high_collateral, 2),
                group2_collateral_pct=round(low_collateral, 2)
            )
            db.add(metric)
        
        # Credit metrics: Good vs Fair
        good_credit_profiles = [p for p in all_profiles if p.cibil_score >= 750]
        fair_credit_profiles = [p for p in all_profiles if 650 <= p.cibil_score < 750]
        
        if good_credit_profiles and fair_credit_profiles:
            good_approvals = sum(1 for p in good_credit_profiles if biased_scores[p.id].approval_decision == "approve")
            fair_approvals = sum(1 for p in fair_credit_profiles if biased_scores[p.id].approval_decision == "approve")
            good_approval_rate = good_approvals / len(good_credit_profiles)
            fair_approval_rate = fair_approvals / len(fair_credit_profiles) if fair_credit_profiles else 0
            approval_parity = good_approval_rate / fair_approval_rate if fair_approval_rate > 0 else 0
            
            good_interest = sum(biased_scores[p.id].interest_rate for p in good_credit_profiles) / len(good_credit_profiles)
            fair_interest = sum(biased_scores[p.id].interest_rate for p in fair_credit_profiles) / len(fair_credit_profiles)
            interest_gap = abs(good_interest - fair_interest)
            
            good_collateral = sum(1 for p in good_credit_profiles if biased_scores[p.id].collateral_required) / len(good_credit_profiles) * 100
            fair_collateral = sum(1 for p in fair_credit_profiles if biased_scores[p.id].collateral_required) / len(fair_credit_profiles) * 100
            collateral_gap = abs(good_collateral - fair_collateral)
            
            fairness_score = 68.0
            severity = SeverityLevel.HIGH
            
            metric = BiasMetric(
                test_run_id=test_run_id,
                dimension=TestDimension.CREDIT,
                approval_parity=round(approval_parity, 3),
                interest_rate_disparity=round(interest_gap, 2),
                collateral_gap=round(collateral_gap, 2),
                edge_case_coverage=95.0,
                overall_fairness_score=round(fairness_score, 2),
                p_value=0.008,
                t_statistic=3.12,
                is_statistically_significant=True,
                confidence_interval_lower=-0.25,
                confidence_interval_upper=-0.12,
                severity=severity,
                group1_name="Good Credit (≥750)",
                group2_name="Fair Credit (650-750)",
                group1_approval_rate=round(good_approval_rate, 3),
                group2_approval_rate=round(fair_approval_rate, 3),
                group1_interest_rate=round(good_interest, 2),
                group2_interest_rate=round(fair_interest, 2),
                group1_collateral_pct=round(good_collateral, 2),
                group2_collateral_pct=round(fair_collateral, 2)
            )
            db.add(metric)
        
        db.commit()
        print("[OK] Created bias metrics")
        
        # Get metrics for feedback
        metrics = db.query(BiasMetric).filter(BiasMetric.test_run_id == test_run_id).all()
        
        print("[6/6] Creating human feedback...")
        if metrics:
            feedback1 = HumanFeedback(
                bias_metric_id=metrics[0].id,
                is_discriminatory="yes",
                root_cause_analysis="The scoring model appears to penalize applicants from rural areas, potentially due to unconscious bias in training data or feature engineering that associates urban locations with lower risk.",
                severity_rating=4,
                suggested_mitigation="1. Remove or reduce geographic location as a direct feature in scoring\n2. Use income-adjusted metrics instead of raw location data\n3. Add explicit fairness constraints for geographic parity\n4. Retrain model with balanced geographic representation",
                annotator_name="Dr. Priya Sharma",
                annotator_role="Senior Loan Officer"
            )
            db.add(feedback1)
            
            if len(metrics) > 1:
                feedback2 = HumanFeedback(
                    bias_metric_id=metrics[1].id,
                    is_discriminatory="yes",
                    root_cause_analysis="Income-based discrimination is evident. The model over-weights family income beyond what's necessary for repayment capacity assessment.",
                    severity_rating=5,
                    suggested_mitigation="1. Cap income influence at repayment capacity threshold\n2. Use income-to-loan ratio instead of absolute income\n3. Consider co-applicant income separately\n4. Add explicit guardrails against income discrimination",
                    annotator_name="Rajesh Kumar",
                    annotator_role="Fairness Consultant"
                )
                db.add(feedback2)
        
        db.commit()
        print("[OK] Created human feedback")
        
        print("Creating mitigation results...")
        if metrics:
            mitigation_run_id = f"MIT_{uuid.uuid4().hex[:8].upper()}"
            
            # Iteration 1
            mitigation1 = MitigationResult(
                mitigation_run_id=mitigation_run_id,
                iteration_number=1,
                prompt_version="fair_v2",
                prompt_text="Refined prompt addressing geographic bias by explicitly ignoring location data...",
                prompt_changes="Added explicit instruction to ignore geographic location. Emphasized income-adjusted metrics.",
                before_fairness_score=75.0,
                after_fairness_score=82.0,
                before_approval_parity=0.89,
                after_approval_parity=0.94,
                before_interest_gap=1.2,
                after_interest_gap=0.8,
                before_collateral_gap=15.0,
                after_collateral_gap=10.0,
                improvement_percentage=9.3,
                target_achieved=False,
                feedback_ids=[1, 2]
            )
            db.add(mitigation1)
            
            # Iteration 2
            mitigation2 = MitigationResult(
                mitigation_run_id=mitigation_run_id,
                iteration_number=2,
                prompt_version="fair_v3",
                prompt_text="Further refined prompt with stronger fairness constraints...",
                prompt_changes="Added explicit guardrails against income discrimination. Strengthened geographic parity requirements.",
                before_fairness_score=82.0,
                after_fairness_score=87.0,
                before_approval_parity=0.94,
                after_approval_parity=0.97,
                before_interest_gap=0.8,
                after_interest_gap=0.5,
                before_collateral_gap=10.0,
                after_collateral_gap=7.0,
                improvement_percentage=6.1,
                target_achieved=True,
                feedback_ids=[1, 2]
            )
            db.add(mitigation2)
        
        db.commit()
        print("[OK] Created mitigation results")
        
        print("\n" + "="*60)
        print("MOCK DATA POPULATION COMPLETE!")
        print("="*60)
        print(f"\nSummary:")
        print(f"   - Test Run ID: {test_run_id}")
        print(f"   - Profiles: {len(profiles)}")
        print(f"   - Scoring Results: {scoring_count}")
        print(f"   - Bias Metrics: {len(metrics)}")
        print(f"   - Human Feedback: {len(db.query(HumanFeedback).all())}")
        print(f"   - Mitigation Results: {len(db.query(MitigationResult).all())}")
        print(f"\nAccess your application:")
        print(f"   - Frontend: http://localhost:3000/dashboard")
        print(f"   - Backend API: http://localhost:8000/docs")
        print("="*60 + "\n")
        
    except Exception as e:
        db.rollback()
        print(f"❌ Error: {e}")
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
    print("Starting mock data population...")
    populate_database()





