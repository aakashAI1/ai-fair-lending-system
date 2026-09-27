#!/usr/bin/env python3
"""
Check test runs in database.
"""

import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from sqlalchemy.orm import Session
from sqlalchemy import desc
from app.database import SessionLocal
from app.models import TestRun, BiasMetric

db = SessionLocal()

try:
    # Get all test runs, ordered by creation time
    test_runs = db.query(TestRun).order_by(desc(TestRun.created_at)).all()
    
    print(f"\n=== TEST RUNS ({len(test_runs)} total) ===\n")
    for i, tr in enumerate(test_runs, 1):
        metrics_count = db.query(BiasMetric).filter(
            BiasMetric.test_run_id == tr.test_run_id
        ).count()
        print(f"{i}. Test Run ID: {tr.test_run_id}")
        print(f"   Created: {tr.created_at}")
        print(f"   Status: {tr.status}")
        print(f"   Metrics: {metrics_count}")
        print()
    
    # Get latest
    latest = db.query(TestRun).order_by(desc(TestRun.created_at)).first()
    if latest:
        print(f"LATEST TEST RUN: {latest.test_run_id}")
        print(f"Created: {latest.created_at}")
        
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
finally:
    db.close()

