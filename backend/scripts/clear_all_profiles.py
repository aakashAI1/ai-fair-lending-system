#!/usr/bin/env python3
"""
URGENT: Clear ALL profiles from database to fix Delhi issue.
Run this before regenerating profiles.
"""

import sys
import io
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

# Fix encoding for Windows
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

from app.database import SessionLocal, init_db
from app.models import StudentProfile, ScoringResult, BiasMetric, HumanFeedback, MitigationResult, TestRun

def clear_all_profiles():
    """Clear ALL profiles and related data."""
    init_db()
    db = SessionLocal()
    
    try:
        print("=" * 70)
        print("CLEARING ALL PROFILES FROM DATABASE")
        print("=" * 70)
        
        # Get counts before deletion
        profile_count = db.query(StudentProfile).count()
        scoring_count = db.query(ScoringResult).count()
        metric_count = db.query(BiasMetric).count()
        feedback_count = db.query(HumanFeedback).count()
        mitigation_count = db.query(MitigationResult).count()
        testrun_count = db.query(TestRun).count()
        
        print(f"\nCurrent database contents:")
        print(f"  - Profiles: {profile_count}")
        print(f"  - Scoring Results: {scoring_count}")
        print(f"  - Bias Metrics: {metric_count}")
        print(f"  - Human Feedback: {feedback_count}")
        print(f"  - Mitigation Results: {mitigation_count}")
        print(f"  - Test Runs: {testrun_count}")
        
        if profile_count == 0:
            print("\n✅ Database is already empty. No action needed.")
            return
        
        print("\n⚠️  DELETING ALL DATA...")
        
        # Delete in order (respecting foreign key constraints)
        print("  - Deleting Mitigation Results...")
        db.query(MitigationResult).delete()
        
        print("  - Deleting Human Feedback...")
        db.query(HumanFeedback).delete()
        
        print("  - Deleting Bias Metrics...")
        db.query(BiasMetric).delete()
        
        print("  - Deleting Scoring Results...")
        db.query(ScoringResult).delete()
        
        print("  - Deleting Student Profiles...")
        db.query(StudentProfile).delete()
        
        print("  - Deleting Test Runs...")
        db.query(TestRun).delete()
        
        db.commit()
        
        print("\n✅ SUCCESS! All profiles and related data cleared!")
        print("\n" + "=" * 70)
        print("NEXT STEPS:")
        print("=" * 70)
        print("1. Run: python scripts\\train_ml_model.py")
        print("   This will regenerate profiles with correct state distribution")
        print("\n2. OR use the UI 'Generate Profiles' button")
        print("   (Make sure backend is running)")
        print("=" * 70 + "\n")
        
    except Exception as e:
        db.rollback()
        print(f"\n❌ Error clearing profiles: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
    finally:
        db.close()

if __name__ == "__main__":
    clear_all_profiles()
