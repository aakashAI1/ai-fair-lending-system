#!/usr/bin/env python3
"""
Train ML model on real datasets for loan approval scoring.
"""

import sys
import os
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

import pandas as pd
import numpy as np
from sqlalchemy.orm import Session
from app.database import SessionLocal, init_db
from app.models import StudentProfile, ScoringResult, BiasMetric, TestRun, TestDimension, ScoringType
from app.services.ml_scoring_model import MLScoringModel
from app.services.deterministic_scoring import DeterministicScoringEngine
from app.services.csv_import_service import csv_import_service
from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize database
init_db()

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
ALL_STATES_WEIGHTED = (
    SOUTHERN_STATES * 57 +
    NORTHERN_STATES * 16 +
    WESTERN_STATES * 12 +
    EASTERN_STATES * 10 +
    NORTHEASTERN_STATES * 5
)

import random
random.shuffle(ALL_STATES_WEIGHTED)


def get_state_for_region(region: str, profile_index: int) -> tuple[str, str]:
    """
    Get state and postcode based on region and profile index.
    Uses research-based distribution (57% Southern states, etc.)
    and cycles through states for diversity.
    """
    # Filter states by region
    region_states = [s for s in ALL_STATES_WEIGHTED if s["region"] == region]
    
    if not region_states:
        # Fallback: use any state from weighted list
        state_info = ALL_STATES_WEIGHTED[profile_index % len(ALL_STATES_WEIGHTED)]
        return state_info["state"], state_info["postcode"]
    
    # Cycle through states in this region for diversity
    state_info = region_states[profile_index % len(region_states)]
    return state_info["state"], state_info["postcode"]


def map_dataset1_to_profile(row: dict) -> dict:
    """Map fair_lending_audit_realistic_500.csv to StudentProfile format."""
    # Convert region
    region_map = {
        'Urban': 'urban_tier1',
        'Semi-Urban': 'rural_tier2',
        'Rural': 'rural_tier3'
    }
    region = region_map.get(row.get('region', 'Urban'), 'urban_tier1')
    
    # Determine test dimension based on data
    if row.get('region') in ['Rural', 'Semi-Urban']:
        test_dim = TestDimension.GEOGRAPHIC
    elif row.get('income_tier') == 'Low':
        test_dim = TestDimension.INCOME
    elif row.get('student_cibil_score', 650) < 600:
        test_dim = TestDimension.CREDIT
    elif row.get('co_app_emp_type') == 'Self-Employed':
        test_dim = TestDimension.EDGE_CASES
    else:
        test_dim = TestDimension.GEOGRAPHIC
    
    # Calculate requested loan amount from FOIR and income
    # FOIR = (EMI / Monthly Income) * 100
    # We'll estimate loan amount from available data
    co_app_income = row.get('co_app_income_annual', 2000000)
    if pd.isna(co_app_income) or co_app_income is None:
        co_app_income = 2000000
    else:
        co_app_income = float(co_app_income)
    existing_emi = row.get('existing_emi_monthly', 0) or 0
    # Rough estimate: requested loan = 10 * annual income (typical for education loans)
    requested_loan = int(co_app_income * 10) if co_app_income else 2000000
    requested_loan = max(500000, min(5000000, requested_loan))
    
    # Map course category to educational background
    course_map = {
        'STEM': 'Engineering',
        'Management': 'Commerce',
        'Medical': 'Science',
        'Data Science': 'Engineering',
        'Arts': 'Arts'
    }
    edu_background = course_map.get(row.get('course_category', 'STEM'), 'Engineering')
    
    # Helper to safely convert to string and handle NaN
    def safe_str(value, default=''):
        if pd.isna(value) or value is None:
            return default
        return str(value)
    
    co_app_rel = safe_str(row.get('co_app_relationship'), 'parent').lower()
    emp_type = safe_str(row.get('co_app_emp_type', 'salaried'), 'salaried').lower()
    
    # Calculate GPA safely (convert to 10-point scale)
    gpa_val = row.get('grad_score_cgpa', 7.0)
    if pd.isna(gpa_val) or gpa_val is None:
        gpa_val = 7.0  # Default to 7.0 on 10-point scale
    else:
        gpa_val = float(gpa_val)
        # If GPA is <= 4.0, assume it's on 4-point scale and convert to 10-point
        if gpa_val > 0 and gpa_val <= 4.0:
            gpa_val = gpa_val * 2.5  # Convert 4-point to 10-point scale
        # Ensure value is within valid 10-point range
        gpa_val = max(5.0, min(10.0, gpa_val))
    
    # Get state and postcode based on research-based distribution (using index from row)
    idx = row.get('_index', hash(str(row)) % 1000)
    state, postcode = get_state_for_region(region, idx)
    
    return {
        'profile_id': row.get('student_id', f"DS1_{hash(str(row))}"),
        'name': f"Student {row.get('student_id', 'Unknown')}",
        'postcode': postcode,
        'region': region,
        'state': state,  # Research-based state distribution
        'family_income': int(co_app_income),
        'cibil_score': int(row.get('student_cibil_score', 650)) if not pd.isna(row.get('student_cibil_score')) else 650,
        'requested_loan_amount': requested_loan,
        'gpa': gpa_val,
        'course': row.get('course_category', 'STEM'),
        'educational_background': edu_background,
        'co_applicant': co_app_rel if co_app_rel else 'parent',
        'employment_type': emp_type if emp_type else 'salaried',
        'family_structure': 'nuclear',  # Default
        'test_dimension': test_dim,
        # Store approval status for training
        '_approval_status': row.get('approval_status', 0),
        '_interest_rate': row.get('interest_rate', None)
    }


def map_dataset2_to_profile(row: dict) -> dict:
    """Map super_loan_dataset_v3_no_interview.csv to StudentProfile format."""
    # Convert Location_Category to region
    location_map = {
        'Urban': 'urban_tier1',
        'Semi-Urban': 'rural_tier2',
        'Rural': 'rural_tier3'
    }
    region = location_map.get(row.get('Location_Category', 'Urban'), 'urban_tier1')
    
    # Determine test dimension
    if row.get('Location_Category') in ['Rural', 'Semi-Urban']:
        test_dim = TestDimension.GEOGRAPHIC
    elif row.get('Community_Category') == 'Group_B':
        test_dim = TestDimension.INCOME  # Assume Group_B = lower income
    elif (row.get('student_cibil_score', 650) and int(row.get('student_cibil_score', 650)) < 600) or row.get('student_cibil_score') == -1:
        test_dim = TestDimension.CREDIT
    elif row.get('co_app_emp_type') == 'Self-Employed':
        test_dim = TestDimension.EDGE_CASES
    else:
        test_dim = TestDimension.GEOGRAPHIC
    
    # Map course category
    course_map = {
        'STEM': 'Engineering',
        'Management': 'Commerce',
        'Medical': 'Science',
        'Arts': 'Arts'
    }
    edu_background = course_map.get(row.get('course_category', 'STEM'), 'Engineering')
    
    # Convert Bank_Decision to approval_status
    bank_decision = str(row.get('Bank_Decision', 'No')).strip()
    approval_status = 1 if bank_decision.lower() == 'yes' else 0
    
    # Get CIBIL score (handle -1 or missing)
    cibil_score = row.get('student_cibil_score')
    if cibil_score == -1 or cibil_score is None or str(cibil_score).strip() == '':
        cibil_score = 650  # Default
    else:
        cibil_score = int(float(cibil_score))
    
    # Get income
    co_app_income = row.get('co_app_income_annual', 0)
    if not co_app_income or co_app_income == 0:
        co_app_income = 2000000  # Default
    else:
        co_app_income = int(float(co_app_income))
    
    # GPA conversion to 10-point scale (if needed)
    gpa = row.get('grad_score_cgpa', 7.0)
    if pd.isna(gpa) or gpa is None or gpa == '':
        gpa = 7.0  # Default to 7.0 on 10-point scale
    else:
        gpa = float(gpa)
        # If GPA is <= 4.0, assume it's on 4-point scale and convert to 10-point
        if gpa > 0 and gpa <= 4.0:
            gpa = gpa * 2.5  # Convert 4-point to 10-point scale
        # Ensure value is within valid 10-point range
        gpa = max(5.0, min(10.0, gpa))
    
    # Helper to safely convert to string and handle NaN
    def safe_str(value, default=''):
        if pd.isna(value) or value is None:
            return default
        return str(value)
    
    co_app_rel = safe_str(row.get('co_app_relationship', 'Father'), 'parent').lower()
    emp_type = safe_str(row.get('co_app_emp_type', 'Salaried'), 'salaried').lower()
    
    # Get state and postcode based on research-based distribution
    idx = row.get('_index', hash(str(row)) % 1000)
    provided_pincode = safe_str(row.get('address_pincode', ''), '')
    if provided_pincode and len(provided_pincode) >= 6:
        postcode = provided_pincode[:6]
        # Still use research-based state mapping
        state, _ = get_state_for_region(region, idx)
    else:
        state, postcode = get_state_for_region(region, idx)
    
    return {
        'profile_id': row.get('student_id', f"DS2_{hash(str(row))}"),
        'name': f"Student {row.get('student_id', 'Unknown')}",
        'postcode': postcode,
        'region': region,
        'state': state,  # Research-based state distribution
        'family_income': co_app_income,
        'cibil_score': cibil_score,
        'requested_loan_amount': int(row.get('total_loan_amount', 2000000)) if row.get('total_loan_amount') else 2000000,
        'gpa': gpa,
        'course': row.get('course_category', 'STEM'),
        'educational_background': edu_background,
        'co_applicant': co_app_rel if co_app_rel else 'parent',
        'employment_type': emp_type if emp_type else 'salaried',
        'family_structure': 'nuclear',  # Default
        'test_dimension': test_dim,
        # Store approval status for training
        '_approval_status': approval_status,
        '_interest_rate': row.get('Interest_Rate', None)
    }


def import_and_train(dataset1_path: Path, dataset2_path: Path):
    """Import datasets, train ML model, and create test run."""
    db = SessionLocal()
    
    try:
        logger.info("=" * 70)
        logger.info("IMPORTING DATASETS AND TRAINING ML MODEL")
        logger.info("=" * 70)
        
        # Clear existing data (optional - comment out if you want to keep existing)
        logger.info("\n[1/7] Clearing existing data...")
        db.query(BiasMetric).delete()
        db.query(ScoringResult).delete()
        db.query(StudentProfile).delete()
        db.query(TestRun).delete()
        db.commit()
        
        # Import Dataset 1
        logger.info("\n[2/7] Importing Dataset 1 (fair_lending_audit_realistic_500.csv)...")
        df1 = pd.read_csv(dataset1_path)
        logger.info(f"   Loaded {len(df1)} records")
        
        profiles_data1 = []
        for idx, row in df1.iterrows():
            # Pass index for state diversity
            row_dict = row.to_dict()
            row_dict['_index'] = idx
            profile_data = map_dataset1_to_profile(row_dict)
            if profile_data:
                profiles_data1.append(profile_data)
        
        logger.info(f"   Mapped {len(profiles_data1)} profiles")
        
        # Import Dataset 2
        logger.info("\n[3/7] Importing Dataset 2 (super_loan_dataset_v3_no_interview.csv)...")
        df2 = pd.read_csv(dataset2_path)
        logger.info(f"   Loaded {len(df2)} records")
        
        profiles_data2 = []
        # Start index from end of dataset 1 for continuous cycling
        start_idx = len(profiles_data1)
        for idx, row in df2.iterrows():
            # Pass index for state diversity (continue from dataset 1)
            row_dict = row.to_dict()
            row_dict['_index'] = start_idx + idx
            profile_data = map_dataset2_to_profile(row_dict)
            if profile_data:
                profiles_data2.append(profile_data)
        
        logger.info(f"   Mapped {len(profiles_data2)} profiles")
        
        # Combine datasets
        all_profiles_data = profiles_data1 + profiles_data2
        logger.info(f"\n   Total profiles: {len(all_profiles_data)}")
        
        # Save profiles to database
        logger.info("\n[4/7] Saving profiles to database...")
        # Store approval statuses separately before popping
        approval_statuses = []
        for profile_data in all_profiles_data:
            # Remove training metadata but store it
            approval_status = profile_data.pop('_approval_status', 0)
            interest_rate = profile_data.pop('_interest_rate', None)
            approval_statuses.append(approval_status)
            
            # Store in profile metadata if needed (we'll use it for training)
            profile = StudentProfile(**profile_data)
            db.add(profile)
        
        db.commit()
        logger.info(f"   Saved {len(all_profiles_data)} profiles")
        
        # Prepare training data
        logger.info("\n[5/7] Preparing training data...")
        # Get all profiles back
        all_profiles = db.query(StudentProfile).all()
        
        # Create DataFrame for training
        training_data = []
        for approval_status, profile in zip(approval_statuses, all_profiles):
            
            training_row = {
                'profile_id': profile.id,
                'gpa': profile.gpa,
                'cibil_score': profile.cibil_score,
                'family_income': profile.family_income,
                'requested_loan_amount': profile.requested_loan_amount,
                'educational_background': profile.educational_background,
                'employment_type': profile.employment_type,
                'co_applicant': profile.co_applicant,
                'family_structure': profile.family_structure,
                'region': profile.region,
                'state': profile.state,
                'approval_decision': 'approve' if approval_status == 1 else 'reject'
            }
            # Only add college_tier if it exists (for backward compatibility)
            if profile.college_tier:
                training_row['college_tier'] = profile.college_tier
            training_data.append(training_row)
        
        train_df = pd.DataFrame(training_data)
        logger.info(f"   Prepared {len(train_df)} training samples")
        logger.info(f"   Approvals: {sum(train_df['approval_decision'] == 'approve')}, Rejections: {sum(train_df['approval_decision'] == 'reject')}")
        
        # Train ML model
        logger.info("\n[6/7] Training ML model...")
        ml_model = MLScoringModel(model_type="random_forest")
        training_metrics = ml_model.train(train_df, target_column="approval_decision")
        logger.info(f"   Model Accuracy: {training_metrics['accuracy']:.3f}")
        logger.info(f"   Model Type: {training_metrics['model_type']}")
        
        # Create test run
        test_run_id = f"TEST_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        test_run = TestRun(
            test_run_id=test_run_id,
            profile_count=len(all_profiles),
            dimensions_tested=[d.value for d in TestDimension],
            status="training",
            progress_percentage=50.0
        )
        db.add(test_run)
        db.commit()
        
        # Score all profiles with trained model
        logger.info("\n[7/7] Scoring profiles with trained ML model...")
        scoring_engine = DeterministicScoringEngine()
        scoring_count = 0
        
        # Score with FAIR model (use deterministic for fair)
        logger.info("   Scoring with FAIR model (deterministic)...")
        for profile in all_profiles:
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
                "college_tier": profile.college_tier if profile.college_tier else "tier3",
                "university_name": profile.university_name if profile.university_name else None,
                "co_applicant": profile.co_applicant,
                "employment_type": profile.employment_type,
                "family_structure": profile.family_structure,
                "test_dimension": profile.test_dimension.value
            }
            
            # Fair scoring (deterministic - unbiased)
            fair_result = scoring_engine.calculate_fair_score(profile_dict)
            fair_scoring = ScoringResult(
                profile_id=profile.id,
                scoring_type=ScoringType.FAIR,
                score=fair_result["score"],
                approval_decision=fair_result["approval_decision"],
                interest_rate=fair_result["interest_rate"],
                collateral_required=fair_result["collateral_required"],
                reasoning=fair_result["reasoning"],
                prompt_version="fair_deterministic_v1"
            )
            db.add(fair_scoring)
            
            # Biased scoring (use trained ML model with bias)
            biased_result = ml_model.predict_score(profile_dict, apply_bias=True)
            biased_scoring = ScoringResult(
                profile_id=profile.id,
                scoring_type=ScoringType.BIASED,
                score=biased_result["score"],
                approval_decision=biased_result["approval_decision"],
                interest_rate=biased_result["interest_rate"],
                collateral_required=biased_result["collateral_required"],
                reasoning=biased_result["reasoning"],
                prompt_version="biased_ml_v1"
            )
            db.add(biased_scoring)
            
            scoring_count += 2
            
            if scoring_count % 100 == 0:
                db.commit()
                logger.info(f"   Scored {scoring_count // 2} profiles...")
        
        db.commit()
        logger.info(f"   Scored {scoring_count} results (fair + biased)")
        
        # Calculate metrics
        logger.info("\n[8/8] Calculating bias metrics...")
        from app.services.metrics_service import MetricsService
        
        metrics_service = MetricsService(db)
        metrics_result = metrics_service.calculate_bias_metrics(
            test_run_id=test_run_id,
            dimensions=list(TestDimension)
        )
        
        metrics = db.query(BiasMetric).filter(
            BiasMetric.test_run_id == test_run_id
        ).all()
        
        # Update test run
        test_run.status = "completed"
        test_run.progress_percentage = 100.0
        test_run.total_profiles_generated = len(all_profiles)
        test_run.total_profiles_scored = scoring_count
        test_run.total_metrics_calculated = len(metrics)
        test_run.completed_at = datetime.now()
        db.commit()
        
        logger.info("\n" + "=" * 70)
        logger.info("TRAINING AND SETUP COMPLETE!")
        logger.info("=" * 70)
        logger.info(f"\nSummary:")
        logger.info(f"   - Test Run ID: {test_run_id}")
        logger.info(f"   - Profiles: {len(all_profiles)}")
        logger.info(f"   - ML Model Accuracy: {training_metrics['accuracy']:.3f}")
        logger.info(f"   - Scoring Results: {scoring_count}")
        logger.info(f"   - Bias Metrics: {len(metrics)}")
        
        if metrics:
            logger.info(f"\nBias Metrics:")
            for metric in metrics[:5]:
                logger.info(f"   - {metric.dimension.value}: Approval Parity={metric.approval_parity:.3f}, "
                          f"Fairness={metric.overall_fairness_score:.1f}/100, Severity={metric.severity.value}")
        
        logger.info(f"\nYour dashboard is ready!")
        logger.info(f"   - Dashboard: http://localhost:3000/dashboard")
        logger.info(f"   - API Docs: http://localhost:8000/docs")
        logger.info("=" * 70 + "\n")
        
    except Exception as e:
        db.rollback()
        logger.error(f"Error: {e}", exc_info=True)
        raise
    finally:
        db.close()


if __name__ == "__main__":
    import sys
    import io
    
    # Fix encoding for Windows
    if sys.platform == "win32":
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
        sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')
    
    # Get dataset paths
    project_root = Path(__file__).parent.parent.parent
    dataset1 = project_root / "fair_lending_audit_realistic_500.csv"
    dataset2 = project_root / "super_loan_dataset_v3_no_interview.csv"
    
    if not dataset1.exists():
        logger.error(f"Dataset 1 not found: {dataset1}")
        sys.exit(1)
    
    if not dataset2.exists():
        logger.error(f"Dataset 2 not found: {dataset2}")
        sys.exit(1)
    
    logger.info("Starting ML model training on real datasets...")
    import_and_train(dataset1, dataset2)

