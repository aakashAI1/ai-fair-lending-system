#!/usr/bin/env python3
"""
Test what the backend sees when it queries the database.
This simulates what the dashboard endpoint does.
"""

import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from sqlalchemy.orm import Session
from sqlalchemy import desc
from app.database import SessionLocal, engine
from app.models import TestRun, BiasMetric

# Check database URL
from app.config import settings
print(f"Database URL: {settings.DATABASE_URL}")
print(f"Engine URL: {engine.url}")

db = SessionLocal()

try:
    # Get latest test run (same as dashboard endpoint)
    test_run = db.query(TestRun).order_by(desc(TestRun.created_at)).first()
    
    if test_run:
        print(f"\nLatest Test Run: {test_run.test_run_id}")
        print(f"Created: {test_run.created_at}")
        
        # Get metrics for this test run
        metrics = db.query(BiasMetric).filter(
            BiasMetric.test_run_id == test_run.test_run_id
        ).all()
        
        print(f"\nMetrics found: {len(metrics)}")
        if metrics:
            print("\nFirst 3 metrics:")
            for m in metrics[:3]:
                print(f"  - {m.dimension.value}: Approval Parity={m.approval_parity}, "
                      f"Interest Gap={m.interest_rate_disparity}, "
                      f"Fairness={m.overall_fairness_score}")
            
            # Calculate averages (same as dashboard)
            approval_parity_avg = sum(m.approval_parity for m in metrics) / len(metrics)
            interest_gap_avg = sum(m.interest_rate_disparity for m in metrics) / len(metrics)
            collateral_gap_avg = sum(m.collateral_gap for m in metrics) / len(metrics)
            
            print(f"\nAverages (what dashboard should show):")
            print(f"  Approval Parity: {approval_parity_avg}")
            print(f"  Interest Gap: {interest_gap_avg}")
            print(f"  Collateral Gap: {collateral_gap_avg}")
    else:
        print("\nNo test runs found!")
        
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
finally:
    db.close()

