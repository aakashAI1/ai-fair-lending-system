#!/usr/bin/env python3
"""
Script to score existing profiles and calculate metrics.
Run this to fix the dashboard when metrics show 0.
"""

import sys
import asyncio
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from app.database import SessionLocal, init_db
from app.models import StudentProfile, ScoringResult, TestRun, ScoringType, TestDimension
from app.services.scoring_service import ScoringService
from app.services.metrics_service import MetricsService
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

init_db()


async def score_and_calculate_metrics():
    """Score all existing profiles and calculate metrics."""
    db = SessionLocal()
    
    try:
        # Get all profiles
        profiles = db.query(StudentProfile).all()
        logger.info(f"Found {len(profiles)} profiles to score")
        
        if len(profiles) == 0:
            logger.warning("No profiles found. Please generate profiles first.")
            return
        
        # Get or create test run
        test_run = db.query(TestRun).order_by(TestRun.created_at.desc()).first()
        if not test_run:
            import uuid
            test_run_id = f"TEST_{uuid.uuid4().hex[:8]}"
            test_run = TestRun(
                test_run_id=test_run_id,
                profile_count=len(profiles),
                dimensions_tested=["geographic", "income", "credit", "edge_cases"],
                status="scoring",
                progress_percentage=0.0
            )
            db.add(test_run)
            db.commit()
            logger.info(f"Created new test run: {test_run_id}")
        else:
            test_run_id = test_run.test_run_id
            logger.info(f"Using existing test run: {test_run_id}")
        
        # Check existing scores
        existing_scores = db.query(ScoringResult).count()
        logger.info(f"Existing scoring results: {existing_scores}")
        
        # Score profiles
        scoring_service = ScoringService(db)
        profile_ids = [p.id for p in profiles]
        
        # Score with FAIR model
        try:
            logger.info(f"Scoring {len(profile_ids)} profiles with FAIR scoring...")
            result = await scoring_service.score_profiles(
                profile_ids=profile_ids,
                scoring_type=ScoringType.FAIR,
                batch_size=100
            )
            logger.info(f"FAIR scoring completed: {result.get('total_scored', 0)} profiles scored")
        except Exception as e:
            logger.error(f"Error in FAIR scoring: {e}", exc_info=True)
            db.rollback()
            raise
        
        # Score with BIASED model
        try:
            logger.info(f"Scoring {len(profile_ids)} profiles with BIASED scoring...")
            result = await scoring_service.score_profiles(
                profile_ids=profile_ids,
                scoring_type=ScoringType.BIASED,
                batch_size=100
            )
            logger.info(f"BIASED scoring completed: {result.get('total_scored', 0)} profiles scored")
        except Exception as e:
            logger.error(f"Error in BIASED scoring: {e}", exc_info=True)
            db.rollback()
            raise
        
        # Calculate metrics
        try:
            logger.info("Calculating bias metrics...")
            metrics_service = MetricsService(db)
            result = metrics_service.calculate_bias_metrics(
                test_run_id=test_run_id,
                dimensions=[
                    TestDimension.GEOGRAPHIC,
                    TestDimension.INCOME,
                    TestDimension.CREDIT,
                    TestDimension.EDGE_CASES
                ]
            )
            logger.info(f"Metrics calculation completed: {result.get('total_metrics', 0)} metrics created")
        except Exception as e:
            logger.error(f"Error calculating metrics: {e}", exc_info=True)
            db.rollback()
            raise
        
        # Update test run status
        test_run.status = "completed"
        test_run.progress_percentage = 100.0
        db.commit()
        
        logger.info("=" * 60)
        logger.info("✅ Successfully scored profiles and calculated metrics!")
        logger.info("=" * 60)
        logger.info(f"Test Run ID: {test_run_id}")
        logger.info(f"Profiles: {len(profiles)}")
        logger.info(f"Scoring Results: {db.query(ScoringResult).count()}")
        logger.info(f"Bias Metrics: {db.query(ScoringResult).count()}")
        logger.info("=" * 60)
        logger.info("🎯 Dashboard should now show metrics!")
        
    except Exception as e:
        logger.error(f"Error: {e}", exc_info=True)
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    logger.info("=" * 60)
    logger.info("Scoring Existing Profiles and Calculating Metrics")
    logger.info("=" * 60)
    asyncio.run(score_and_calculate_metrics())
