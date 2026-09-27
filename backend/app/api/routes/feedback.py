"""
API routes for human feedback.
"""

import logging
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.deps import get_database
from app.models import HumanFeedback, BiasMetric
from app.schemas import HumanFeedbackCreate, HumanFeedbackResponse
from app.services.genai_service import genai_service

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/feedback", tags=["feedback"])


@router.post("/", response_model=HumanFeedbackResponse)
async def submit_feedback(
    feedback: HumanFeedbackCreate,
    db: Session = Depends(get_database)
):
    """
    Submit human feedback for a bias finding.
    """
    try:
        # Validate bias metric exists
        bias_metric = db.query(BiasMetric).filter(
            BiasMetric.id == feedback.bias_metric_id
        ).first()
        
        if not bias_metric:
            raise HTTPException(status_code=404, detail="Bias metric not found")
        
        # Create feedback
        db_feedback = HumanFeedback(
            bias_metric_id=feedback.bias_metric_id,
            is_discriminatory=feedback.is_discriminatory,
            root_cause_analysis=feedback.root_cause_analysis,
            severity_rating=feedback.severity_rating,
            suggested_mitigation=feedback.suggested_mitigation,
            annotator_name=feedback.annotator_name,
            annotator_role=feedback.annotator_role
        )
        db.add(db_feedback)
        db.commit()
        db.refresh(db_feedback)
        
        return HumanFeedbackResponse.model_validate(db_feedback)
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        logger.error(f"Error submitting feedback: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/", response_model=List[HumanFeedbackResponse])
async def list_feedback(
    bias_metric_id: int = None,
    db: Session = Depends(get_database)
):
    """
    List human feedback.
    """
    try:
        query = db.query(HumanFeedback)
        if bias_metric_id:
            query = query.filter(HumanFeedback.bias_metric_id == bias_metric_id)
        feedbacks = query.all()
        return [HumanFeedbackResponse.model_validate(f) for f in feedbacks]
    except Exception as e:
        logger.error(f"Error listing feedback: {e}", exc_info=True)
        # Return empty list instead of error
        return []


@router.post("/suggest-mitigation/{metric_id}")
async def suggest_mitigation(
    metric_id: int,
    db: Session = Depends(get_database)
):
    """
    Get AI-powered mitigation suggestions for a bias metric.
    """
    try:
        # Get the bias metric
        metric = db.query(BiasMetric).filter(BiasMetric.id == metric_id).first()
        if not metric:
            raise HTTPException(status_code=404, detail="Bias metric not found")
        
        # Generate suggestions using GenAI
        suggestions = await genai_service.suggest_mitigation(
            group1_name=metric.group1_name,
            group2_name=metric.group2_name,
            dimension=metric.dimension.value,
            approval_parity=metric.approval_parity,
            interest_gap=metric.interest_rate_disparity,
            collateral_gap=metric.collateral_gap,
            fairness_score=metric.overall_fairness_score,
            severity=metric.severity.value
        )
        
        return suggestions
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error generating mitigation suggestions: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{feedback_id}", response_model=HumanFeedbackResponse)
async def get_feedback(
    feedback_id: int,
    db: Session = Depends(get_database)
):
    """
    Get a specific feedback.
    """
    try:
        feedback = db.query(HumanFeedback).filter(
            HumanFeedback.id == feedback_id
        ).first()
        
        if not feedback:
            raise HTTPException(status_code=404, detail="Feedback not found")
        
        return HumanFeedbackResponse.model_validate(feedback)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting feedback: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

