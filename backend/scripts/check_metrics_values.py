#!/usr/bin/env python3
"""
Script to check actual metric values in the database.
"""

import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models import BiasMetric, ScoringResult, StudentProfile
from app.models import ScoringType

db = SessionLocal()

try:
    # Get all metrics
    metrics = db.query(BiasMetric).all()
    print(f"\n=== BIAS METRICS ({len(metrics)} total) ===\n")
    
    for i, m in enumerate(metrics, 1):
        print(f"Metric {i}:")
        print(f"  Dimension: {m.dimension.value}")
        print(f"  Approval Parity: {m.approval_parity}")
        print(f"  Interest Rate Disparity: {m.interest_rate_disparity}")
        print(f"  Collateral Gap: {m.collateral_gap}")
        print(f"  Fairness Score: {m.overall_fairness_score}")
        print(f"  Group1: {m.group1_name} (approval: {m.group1_approval_rate:.2%})")
        print(f"  Group2: {m.group2_name} (approval: {m.group2_approval_rate:.2%})")
        print()
    
    # Check scoring results
    fair_scores = db.query(ScoringResult).filter(
        ScoringResult.scoring_type == ScoringType.FAIR
    ).all()
    biased_scores = db.query(ScoringResult).filter(
        ScoringResult.scoring_type == ScoringType.BIASED
    ).all()
    
    print(f"\n=== SCORING RESULTS ===\n")
    print(f"Fair scores: {len(fair_scores)}")
    print(f"Biased scores: {len(biased_scores)}")
    
    if fair_scores:
        approved_fair = sum(1 for s in fair_scores if s.approval_decision == 'approve')
        print(f"Fair approvals: {approved_fair}/{len(fair_scores)} ({approved_fair/len(fair_scores):.2%})")
    
    if biased_scores:
        approved_biased = sum(1 for s in biased_scores if s.approval_decision == 'approve')
        print(f"Biased approvals: {approved_biased}/{len(biased_scores)} ({approved_biased/len(biased_scores):.2%})")
    
    # Check if profiles exist
    profile_count = db.query(StudentProfile).count()
    print(f"\nProfiles in database: {profile_count}")
    
except Exception as e:
    print(f"[ERROR] Error: {e}")
    import traceback
    traceback.print_exc()
finally:
    db.close()

