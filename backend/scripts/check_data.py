#!/usr/bin/env python3
"""
Quick script to check if data exists in the database.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models import StudentProfile, TestRun, BiasMetric, ScoringResult

db = SessionLocal()

try:
    # Check profiles
    profile_count = db.query(StudentProfile).count()
    print(f"[OK] Profiles: {profile_count}")
    
    # Check test runs
    test_runs = db.query(TestRun).all()
    print(f"[OK] Test Runs: {len(test_runs)}")
    for tr in test_runs:
        print(f"  - {tr.test_run_id} (status: {tr.status}, created: {tr.created_at})")
    
    # Check scoring results
    scoring_count = db.query(ScoringResult).count()
    print(f"[OK] Scoring Results: {scoring_count}")
    
    # Check bias metrics
    metrics = db.query(BiasMetric).all()
    print(f"[OK] Bias Metrics: {len(metrics)}")
    for m in metrics:
        print(f"  - {m.dimension.value} (test_run: {m.test_run_id}, fairness: {m.overall_fairness_score:.1f})")
    
    if len(test_runs) > 0:
        latest_test_run = test_runs[0]
        metrics_for_run = db.query(BiasMetric).filter(
            BiasMetric.test_run_id == latest_test_run.test_run_id
        ).all()
        print(f"\n[OK] Metrics for latest test run ({latest_test_run.test_run_id}): {len(metrics_for_run)}")
    
except Exception as e:
    print(f"[ERROR] Error: {e}")
    import traceback
    traceback.print_exc()
finally:
    db.close()

