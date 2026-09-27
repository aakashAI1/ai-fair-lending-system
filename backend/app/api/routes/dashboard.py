"""
API routes for dashboard data.
"""

import logging
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import desc

from app.api.deps import get_database
from app.models import BiasMetric, TestRun, StudentProfile, TestDimension, ScoringResult, ScoringType
from app.schemas import DashboardResponse, KPIMetrics, TopFinding
from app.database import SessionLocal

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/dashboard", tags=["dashboard"])


@router.get("", response_model=DashboardResponse)
async def get_dashboard(
    test_run_id: Optional[str] = Query(None),
    db: Session = Depends(get_database)
):
    """
    Get dashboard data including KPIs, top findings, and heatmap.
    """
    try:
        # First check if there are any student profiles
        profile_count = db.query(StudentProfile).count()
        if profile_count == 0:
            # No profiles uploaded yet - return empty dashboard
            from app.models import SeverityLevel
            from datetime import datetime
            return DashboardResponse(
                kpi_metrics=KPIMetrics(
                    approval_parity=0.0,
                    interest_gap=0.0,
                    collateral_gap=0.0,
                    fairness_score=0.0,
                    severity=SeverityLevel.LOW
                ),
                top_findings=[],
                heatmap_data={},
                test_run_id="",
                last_updated=datetime.now()
            )
        
        # Get latest test run if not specified
        if not test_run_id:
            test_run = db.query(TestRun).order_by(desc(TestRun.created_at)).first()
            if test_run:
                test_run_id = test_run.test_run_id
            else:
                # Profiles exist but no test run yet - return empty dashboard
                from app.models import SeverityLevel
                from datetime import datetime
                return DashboardResponse(
                    kpi_metrics=KPIMetrics(
                        approval_parity=0.0,
                        interest_gap=0.0,
                        collateral_gap=0.0,
                        fairness_score=0.0,
                        severity=SeverityLevel.LOW
                    ),
                    top_findings=[],
                    heatmap_data={},
                    test_run_id="",
                    last_updated=datetime.now()
                )
        
        # Get metrics for this test run
        metrics = db.query(BiasMetric).filter(
            BiasMetric.test_run_id == test_run_id
        ).all()
        
        # If no metrics for current test run, get latest metrics from ANY test run
        if not metrics:
            logger.info(f"No metrics found for test_run_id: {test_run_id}. Looking for latest metrics...")
            latest_metric = db.query(BiasMetric).order_by(desc(BiasMetric.created_at)).first()
            if latest_metric:
                # Use the test run ID from the latest metric
                metrics = db.query(BiasMetric).filter(
                    BiasMetric.test_run_id == latest_metric.test_run_id
                ).all()
                test_run_id = latest_metric.test_run_id
                logger.info(f"Found {len(metrics)} metrics from test_run_id: {test_run_id}")
        
        if not metrics:
            # No metrics yet - check if we need to score profiles and calculate metrics
            # Check if profiles have scoring results
            from app.models import ScoringResult, ScoringType
            fair_scores = db.query(ScoringResult).filter(
                ScoringResult.scoring_type == ScoringType.FAIR
            ).count()
            biased_scores = db.query(ScoringResult).filter(
                ScoringResult.scoring_type == ScoringType.BIASED
            ).count()
            
            # If profiles exist but no scores, trigger scoring in background
            if profile_count > 0 and (fair_scores == 0 or biased_scores == 0):
                logger.info(f"Profiles exist ({profile_count}) but no scoring results. Triggering automatic scoring...")
                from fastapi import BackgroundTasks
                from app.services.scoring_service import ScoringService
                from app.services.metrics_service import MetricsService
                import asyncio
                
                async def auto_score_and_metrics():
                    bg_db = SessionLocal()
                    try:
                        scoring_service = ScoringService(bg_db)
                        profile_ids = [p.id for p in bg_db.query(StudentProfile).all()]
                        
                        # Score with FAIR
                        if fair_scores == 0:
                            logger.info("Auto-scoring with FAIR model...")
                            await scoring_service.score_profiles(
                                profile_ids=profile_ids,
                                scoring_type=ScoringType.FAIR,
                                batch_size=100
                            )
                        
                        # Score with BIASED
                        if biased_scores == 0:
                            logger.info("Auto-scoring with BIASED model...")
                            await scoring_service.score_profiles(
                                profile_ids=profile_ids,
                                scoring_type=ScoringType.BIASED,
                                batch_size=100
                            )
                        
                        # Calculate metrics
                        logger.info("Auto-calculating metrics...")
                        metrics_service = MetricsService(bg_db)
                        metrics_service.calculate_bias_metrics(
                            test_run_id=test_run_id,
                            dimensions=[
                                TestDimension.GEOGRAPHIC,
                                TestDimension.INCOME,
                                TestDimension.CREDIT,
                                TestDimension.EDGE_CASES
                            ]
                        )
                        logger.info("Auto-scoring and metrics calculation completed")
                    except Exception as e:
                        logger.error(f"Error in auto-scoring: {e}", exc_info=True)
                    finally:
                        bg_db.close()
                
                # Run async task in background (non-blocking)
                import asyncio
                try:
                    loop = asyncio.get_event_loop()
                except RuntimeError:
                    loop = asyncio.new_event_loop()
                    asyncio.set_event_loop(loop)
                
                if loop.is_running():
                    # If loop is running, create task
                    asyncio.create_task(auto_score_and_metrics())
                else:
                    # Otherwise run in thread
                    import threading
                    def run_in_thread():
                        new_loop = asyncio.new_event_loop()
                        asyncio.set_event_loop(new_loop)
                        new_loop.run_until_complete(auto_score_and_metrics())
                        new_loop.close()
                    threading.Thread(target=run_in_thread, daemon=True).start()
            
            # Return empty dashboard data (will update after scoring completes)
            from app.models import SeverityLevel
            from datetime import datetime
            test_run = db.query(TestRun).filter(
                TestRun.test_run_id == test_run_id
            ).first()
            return DashboardResponse(
                kpi_metrics=KPIMetrics(
                    approval_parity=0.0,
                    interest_gap=0.0,
                    collateral_gap=0.0,
                    fairness_score=0.0,
                    severity=SeverityLevel.LOW
                ),
                top_findings=[],
                heatmap_data={},
                test_run_id=test_run_id or "",
                last_updated=test_run.created_at if test_run else datetime.now()
            )
        
        # Calculate KPIs (average across all metrics)
        approval_parity_avg = sum(m.approval_parity for m in metrics) / len(metrics)
        interest_gap_avg = sum(m.interest_rate_disparity for m in metrics) / len(metrics)
        collateral_gap_avg = sum(m.collateral_gap for m in metrics) / len(metrics)
        fairness_score_avg = sum(m.overall_fairness_score for m in metrics) / len(metrics)
        
        # Determine overall severity
        max_severity = max(metrics, key=lambda m: {
            "critical": 4, "high": 3, "medium": 2, "low": 1
        }.get(m.severity.value, 0))
        overall_severity = max_severity.severity
        
        kpi_metrics = KPIMetrics(
            approval_parity=approval_parity_avg,
            interest_gap=interest_gap_avg,
            collateral_gap=collateral_gap_avg,
            fairness_score=fairness_score_avg,
            severity=overall_severity
        )
        
        # Get top 3 findings (by severity)
        sorted_metrics = sorted(
            metrics,
            key=lambda m: {
                "critical": 4, "high": 3, "medium": 2, "low": 1
            }.get(m.severity.value, 0),
            reverse=True
        )
        
        top_findings = []
        for metric in sorted_metrics[:3]:
            finding = TopFinding(
                id=metric.id,
                dimension=metric.dimension,
                description=f"{metric.group1_name} vs {metric.group2_name}: Approval parity {metric.approval_parity:.2f}",
                severity=metric.severity,
                metric_value=metric.overall_fairness_score,
                group1_name=metric.group1_name,
                group2_name=metric.group2_name,
                group1_value=metric.group1_approval_rate,
                group2_value=metric.group2_approval_rate
            )
            top_findings.append(finding)
        
        # Create heatmap data (dimension vs severity)
        heatmap_data = {}
        for metric in metrics:
            dimension = metric.dimension.value
            if dimension not in heatmap_data:
                heatmap_data[dimension] = {}
            severity = metric.severity.value
            if severity not in heatmap_data[dimension]:
                heatmap_data[dimension][severity] = 0
            heatmap_data[dimension][severity] += 1
        
        # Get test run for timestamp
        test_run = db.query(TestRun).filter(
            TestRun.test_run_id == test_run_id
        ).first()
        
        from datetime import datetime
        return DashboardResponse(
            kpi_metrics=kpi_metrics,
            top_findings=top_findings,
            heatmap_data=heatmap_data,
            test_run_id=test_run_id,
            last_updated=test_run.created_at if test_run else datetime.now()
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting dashboard data: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

