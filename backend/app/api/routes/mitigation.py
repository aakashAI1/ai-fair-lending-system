"""
API routes for bias mitigation.
"""

import logging
from typing import List
from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session

from app.api.deps import get_database, require_admin
from app.models import MitigationResult, User
from app.schemas import (
    MitigationRequest,
    MitigationComparisonResponse,
    MitigationResultResponse
)
from app.services.mitigation_service import MitigationService

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/mitigation", tags=["mitigation"])


@router.post("/run", response_model=MitigationComparisonResponse)
async def run_mitigation(
    request: MitigationRequest,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_database)
):
    """
    Run iterative mitigation cycle.
    """
    try:
        mitigation_service = MitigationService(db)
        
        # Run mitigation
        result = await mitigation_service.run_mitigation_cycle(
            test_run_id=request.test_run_id,
            feedback_ids=request.feedback_ids,
            max_iterations=request.max_iterations,
            target_fairness_score=request.target_fairness_score
        )
        
        # Get mitigation results
        mitigation_results = db.query(MitigationResult).filter(
            MitigationResult.mitigation_run_id == result["mitigation_run_id"]
        ).order_by(MitigationResult.iteration_number).all()
        
        return MitigationComparisonResponse(
            mitigation_run_id=result["mitigation_run_id"],
            iterations=[MitigationResultResponse.model_validate(r) for r in mitigation_results],
            initial_fairness_score=result["initial_fairness_score"],
            final_fairness_score=result["final_fairness_score"],
            total_improvement=result["improvement_percentage"],
            target_achieved=result["target_achieved"]
        )
        
    except Exception as e:
        logger.error(f"Error running mitigation: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/history/{mitigation_run_id}", response_model=MitigationComparisonResponse)
async def get_mitigation_history(
    mitigation_run_id: str,
    db: Session = Depends(get_database)
):
    """
    Get mitigation history for a run.
    """
    try:
        mitigation_results = db.query(MitigationResult).filter(
            MitigationResult.mitigation_run_id == mitigation_run_id
        ).order_by(MitigationResult.iteration_number).all()
        
        if not mitigation_results:
            raise HTTPException(status_code=404, detail="Mitigation run not found")
        
        initial_result = mitigation_results[0]
        final_result = mitigation_results[-1]
        
        # Calculate improvement percentage (ensure always positive)
        initial_score = initial_result.before_fairness_score or 0.0
        final_score = final_result.after_fairness_score
        if initial_score > 0:
            improvement_pct = max(0.0, ((final_score - initial_score) / initial_score) * 100)
        else:
            improvement_pct = 0.0
        
        return MitigationComparisonResponse(
            mitigation_run_id=mitigation_run_id,
            iterations=[MitigationResultResponse.model_validate(r) for r in mitigation_results],
            initial_fairness_score=initial_score,
            final_fairness_score=final_score,
            total_improvement=improvement_pct,
            target_achieved=final_result.target_achieved
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting mitigation history: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/", response_model=List[dict])
async def list_mitigation_runs(
    db: Session = Depends(get_database),
    current_user: User = require_admin()
):
    """
    List all unique mitigation runs (grouped by mitigation_run_id).
    Returns summary info for each run.
    """
    try:
        from sqlalchemy import func
        
        # Get all unique mitigation_run_ids with summary info
        runs = db.query(
            MitigationResult.mitigation_run_id,
            func.min(MitigationResult.created_at).label('created_at'),
            func.max(MitigationResult.iteration_number).label('total_iterations'),
            func.min(MitigationResult.before_fairness_score).label('initial_score'),
            func.max(MitigationResult.after_fairness_score).label('final_score'),
            func.max(MitigationResult.after_fairness_score - MitigationResult.before_fairness_score).label('total_improvement'),
            func.max(MitigationResult.target_achieved).label('target_achieved')
        ).group_by(MitigationResult.mitigation_run_id).order_by(func.min(MitigationResult.created_at).desc()).all()
        
        result = []
        for run in runs:
            # Get first result to get feedback_ids
            first_result = db.query(MitigationResult).filter(
                MitigationResult.mitigation_run_id == run.mitigation_run_id
            ).order_by(MitigationResult.iteration_number).first()
            
            # Calculate improvement percentage (ensure always positive)
            initial_score = float(run.initial_score or 0)
            final_score = float(run.final_score or 0)
            if initial_score > 0:
                improvement_pct = max(0.0, ((final_score - initial_score) / initial_score) * 100)
            else:
                improvement_pct = 0.0
            
            result.append({
                "mitigation_run_id": run.mitigation_run_id,
                "created_at": run.created_at.isoformat() if run.created_at else None,
                "total_iterations": run.total_iterations or 0,
                "initial_score": initial_score,
                "final_score": final_score,
                "total_improvement": float(run.total_improvement or 0),
                "improvement_percentage": improvement_pct,
                "target_achieved": bool(run.target_achieved),
                "feedback_ids": first_result.feedback_ids if first_result else []
            })
        
        return result
    except Exception as e:
        logger.error(f"Error listing mitigation runs: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/detail/{mitigation_run_id}", response_model=dict)
async def get_mitigation_detail(
    mitigation_run_id: str,
    db: Session = Depends(get_database)
):
    """
    Get detailed mitigation information including all iterations and feedback details.
    """
    try:
        from app.models import HumanFeedback
        
        # Get all iterations for this run
        mitigation_results = db.query(MitigationResult).filter(
            MitigationResult.mitigation_run_id == mitigation_run_id
        ).order_by(MitigationResult.iteration_number).all()
        
        if not mitigation_results:
            raise HTTPException(status_code=404, detail="Mitigation run not found")
        
        # Get first result to get feedback_ids
        first_result = mitigation_results[0]
        feedback_ids = first_result.feedback_ids or []
        
        # Get detailed feedback information
        feedbacks = []
        if feedback_ids:
            feedback_entries = db.query(HumanFeedback).filter(
                HumanFeedback.id.in_(feedback_ids)
            ).all()
            
            for feedback in feedback_entries:
                feedbacks.append({
                    "id": feedback.id,
                    "annotator_name": feedback.annotator_name or "Unknown",
                    "annotator_role": feedback.annotator_role or "Unknown",
                    "is_discriminatory": feedback.is_discriminatory,
                    "severity_rating": feedback.severity_rating,
                    "root_cause_analysis": feedback.root_cause_analysis,
                    "suggested_mitigation": feedback.suggested_mitigation,
                    "created_at": feedback.created_at.isoformat() if feedback.created_at else None,
                    "bias_metric_id": feedback.bias_metric_id
                })
        
        # Get bias metrics for the test run to include group-specific data
        from app.models import BiasMetric
        bias_metrics = []
        initial_metrics_snapshot = []  # Store initial state for comparison
        
        if mitigation_results:
            first_result = mitigation_results[0]
            # Get test_run_id from feedbacks
            test_run_id = None
            if feedback_ids:
                first_feedback = db.query(HumanFeedback).filter(HumanFeedback.id == feedback_ids[0]).first()
                if first_feedback:
                    metric = db.query(BiasMetric).filter(BiasMetric.id == first_feedback.bias_metric_id).first()
                    if metric:
                        test_run_id = metric.test_run_id
            
            if test_run_id:
                # Get the FIRST mitigation result's before_approval_parity to find initial state
                # Use the iteration data stored in MitigationResult to get initial metrics
                first_iteration = mitigation_results[0]
                
                # Get ALL metrics for this test run, ordered by creation time
                all_metrics = db.query(BiasMetric).filter(
                    BiasMetric.test_run_id == test_run_id
                ).order_by(BiasMetric.created_at.asc(), BiasMetric.id.asc()).all()
                
                # Group by (dimension, group1_name, group2_name) and get FIRST (initial) and LAST (final)
                metric_groups = {}
                for m in all_metrics:
                    key = (m.dimension, m.group1_name, m.group2_name)
                    if key not in metric_groups:
                        metric_groups[key] = {"initial": m, "final": m}
                    else:
                        metric_groups[key]["final"] = m  # Update to latest (after mitigation)
                
                # Build initial and final metrics - use the ones that match the first iteration's before values
                for key, group_metrics in metric_groups.items():
                    initial = group_metrics["initial"]
                    final = group_metrics["final"]
                    
                    # Calculate proper approval parity (min/max ratio, not group1/group2)
                    initial_rate1 = float(initial.group1_approval_rate)
                    initial_rate2 = float(initial.group2_approval_rate)
                    final_rate1 = float(final.group1_approval_rate)
                    final_rate2 = float(final.group2_approval_rate)
                    
                    initial_min = min(initial_rate1, initial_rate2)
                    initial_max = max(initial_rate1, initial_rate2)
                    final_min = min(final_rate1, final_rate2)
                    final_max = max(final_rate1, final_rate2)
                    
                    initial_parity = (initial_min / initial_max) if initial_max > 0 else 0.0
                    final_parity = (final_min / final_max) if final_max > 0 else 0.0
                    
                    # Initial snapshot (before mitigation)
                    initial_metrics_snapshot.append({
                        "dimension": initial.dimension.value,
                        "group1_name": initial.group1_name,
                        "group2_name": initial.group2_name,
                        "group1_approval_rate": initial_rate1,
                        "group2_approval_rate": initial_rate2,
                        "approval_parity": initial_parity,
                        "group1_interest_rate": float(initial.group1_interest_rate),
                        "group2_interest_rate": float(initial.group2_interest_rate),
                        "interest_rate_disparity": float(initial.interest_rate_disparity),
                        "collateral_gap": float(initial.collateral_gap),
                    })
                    
                    # Final metrics (after mitigation)
                    bias_metrics.append({
                        "dimension": final.dimension.value,
                        "group1_name": final.group1_name,
                        "group2_name": final.group2_name,
                        "group1_approval_rate": final_rate1,
                        "group2_approval_rate": final_rate2,
                        "approval_parity": final_parity,
                        "group1_interest_rate": float(final.group1_interest_rate),
                        "group2_interest_rate": float(final.group2_interest_rate),
                        "interest_rate_disparity": float(final.interest_rate_disparity),
                        "collateral_gap": float(final.collateral_gap),
                    })
        
        # Build detailed response
        iterations = []
        for result in mitigation_results:
            iterations.append({
                "id": result.id,
                "iteration_number": result.iteration_number,
                "prompt_version": result.prompt_version,
                "prompt_text": result.prompt_text,
                "prompt_changes": result.prompt_changes,
                "before_fairness_score": float(result.before_fairness_score or 0),
                "after_fairness_score": float(result.after_fairness_score),
                "before_approval_parity": float(result.before_approval_parity or 0),
                "after_approval_parity": float(result.after_approval_parity),
                "before_interest_gap": float(result.before_interest_gap or 0),
                "after_interest_gap": float(result.after_interest_gap),
                "before_collateral_gap": float(result.before_collateral_gap or 0),
                "after_collateral_gap": float(result.after_collateral_gap),
                "improvement_percentage": float(result.improvement_percentage),
                "target_achieved": result.target_achieved,
                "created_at": result.created_at.isoformat() if result.created_at else None
            })
        
        initial_result = mitigation_results[0]
        final_result = mitigation_results[-1]
        
        # Get test_run_id from feedback if available
        test_run_id = None
        if feedback_ids:
            first_feedback = db.query(HumanFeedback).filter(HumanFeedback.id == feedback_ids[0]).first()
            if first_feedback:
                metric = db.query(BiasMetric).filter(BiasMetric.id == first_feedback.bias_metric_id).first()
                if metric:
                    test_run_id = metric.test_run_id
        
        # Calculate improvement percentage (ensure always positive)
        initial_score = float(initial_result.before_fairness_score or 0)
        final_score = float(final_result.after_fairness_score)
        if initial_score > 0:
            improvement_pct = max(0.0, ((final_score - initial_score) / initial_score) * 100)
        else:
            improvement_pct = 0.0
        
        return {
            "mitigation_run_id": mitigation_run_id,
            "test_run_id": test_run_id,
            "created_at": initial_result.created_at.isoformat() if initial_result.created_at else None,
            "total_iterations": len(mitigation_results),
            "initial_fairness_score": initial_score,
            "final_fairness_score": final_score,
            "total_improvement": float(final_score - initial_score),
            "improvement_percentage": improvement_pct,
            "target_achieved": final_result.target_achieved,
            "iterations": iterations,
            "feedbacks": feedbacks,
            "feedback_ids": feedback_ids,
            "metrics": bias_metrics,  # Final metrics (after mitigation)
            "initial_metrics": initial_metrics_snapshot  # Initial metrics (before mitigation)
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting mitigation detail: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))







