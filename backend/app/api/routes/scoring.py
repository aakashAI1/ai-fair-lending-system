"""
API routes for scoring profiles.
"""

import logging
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session

from app.api.deps import get_database
from app.models import ScoringResult, ScoringType
from app.schemas import (
    ScoringRequest,
    ScoringBatchResponse,
    ScoringResultResponse
)
from app.services.scoring_service import ScoringService

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/scoring", tags=["scoring"])


@router.post("/fair", response_model=ScoringBatchResponse)
async def score_fair(
    request: ScoringRequest,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_database)
):
    """
    Score profiles using fair (unbiased) scoring model.
    """
    try:
        scoring_service = ScoringService(db)
        
        # Score profiles
        result = await scoring_service.score_profiles(
            profile_ids=request.profile_ids,
            scoring_type=ScoringType.FAIR,
            batch_size=request.batch_size,
            prompt_version="fair_v1"
        )
        
        # Get scoring results
        scoring_results = scoring_service.get_scoring_results(
            scoring_type=ScoringType.FAIR
        )
        
        return ScoringBatchResponse(
            total_scored=result["total_scored"],
            successful=result["successful"],
            failed=result["failed"],
            results=[ScoringResultResponse.model_validate(r) for r in scoring_results],
            errors=result["errors"]
        )
        
    except Exception as e:
        logger.error(f"Error in score_fair: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/biased", response_model=ScoringBatchResponse)
async def score_biased(
    request: ScoringRequest,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_database)
):
    """
    Score profiles using biased scoring model.
    """
    try:
        scoring_service = ScoringService(db)
        
        # Score profiles
        result = await scoring_service.score_profiles(
            profile_ids=request.profile_ids,
            scoring_type=ScoringType.BIASED,
            batch_size=request.batch_size,
            prompt_version="biased_v1"
        )
        
        # Get scoring results
        scoring_results = scoring_service.get_scoring_results(
            scoring_type=ScoringType.BIASED
        )
        
        return ScoringBatchResponse(
            total_scored=result["total_scored"],
            successful=result["successful"],
            failed=result["failed"],
            results=[ScoringResultResponse.model_validate(r) for r in scoring_results],
            errors=result["errors"]
        )
        
    except Exception as e:
        logger.error(f"Error in score_biased: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/results", response_model=List[ScoringResultResponse])
async def get_scoring_results(
    profile_id: Optional[int] = None,
    scoring_type: Optional[ScoringType] = None,
    db: Session = Depends(get_database)
):
    """
    Get scoring results.
    """
    try:
        scoring_service = ScoringService(db)
        results = scoring_service.get_scoring_results(
            profile_id=profile_id,
            scoring_type=scoring_type
        )
        return [ScoringResultResponse.model_validate(r) for r in results]
    except Exception as e:
        logger.error(f"Error getting scoring results: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/comparison/{profile_id}")
async def get_profile_comparison(
    profile_id: int,
    db: Session = Depends(get_database)
):
    """
    Get fair vs biased comparison for a profile.
    """
    try:
        scoring_service = ScoringService(db)
        comparison = scoring_service.get_profile_comparison(profile_id)
        return comparison
    except Exception as e:
        logger.error(f"Error getting profile comparison: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))







