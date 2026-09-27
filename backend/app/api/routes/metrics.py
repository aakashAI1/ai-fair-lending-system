"""
API routes for bias metrics calculation and retrieval.
"""

import logging
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.deps import get_database
from app.models import BiasMetric, TestDimension, StudentProfile, ScoringResult, ScoringType
from app.schemas import (
    MetricsCalculationRequest,
    MetricsSummaryResponse,
    BiasMetricResponse,
    StudentProfileResponse,
    ScoringResultResponse
)
from app.services.metrics_service import MetricsService
from sqlalchemy import or_, and_
from typing import Dict, Any, List

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/metrics", tags=["metrics"])


@router.post("/calculate", response_model=MetricsSummaryResponse)
async def calculate_metrics(
    request: MetricsCalculationRequest,
    db: Session = Depends(get_database)
):
    """
    Calculate bias metrics for a test run.
    """
    try:
        metrics_service = MetricsService(db)
        
        # Calculate metrics
        result = metrics_service.calculate_bias_metrics(
            test_run_id=request.test_run_id,
            dimensions=request.dimensions
        )
        
        # Get all metrics for this test run
        metrics = db.query(BiasMetric).filter(
            BiasMetric.test_run_id == request.test_run_id
        ).all()
        
        # Calculate summary
        overall_fairness_score = sum(m.overall_fairness_score for m in metrics) / len(metrics) if metrics else 0.0
        critical_findings = len([m for m in metrics if m.severity.value == "critical"])
        high_findings = len([m for m in metrics if m.severity.value == "high"])
        medium_findings = len([m for m in metrics if m.severity.value == "medium"])
        low_findings = len([m for m in metrics if m.severity.value == "low"])
        
        return MetricsSummaryResponse(
            test_run_id=request.test_run_id,
            total_metrics=len(metrics),
            metrics=[BiasMetricResponse.model_validate(m) for m in metrics],
            overall_fairness_score=overall_fairness_score,
            critical_findings=critical_findings,
            high_findings=high_findings,
            medium_findings=medium_findings,
            low_findings=low_findings
        )
        
    except Exception as e:
        logger.error(f"Error calculating metrics: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/detail/{metric_id}", response_model=BiasMetricResponse)
async def get_metric_detail(
    metric_id: int,
    db: Session = Depends(get_database)
):
    """
    Get detailed information for a specific bias metric.
    """
    try:
        metric = db.query(BiasMetric).filter(BiasMetric.id == metric_id).first()
        if not metric:
            raise HTTPException(status_code=404, detail="Metric not found")
        return BiasMetricResponse.model_validate(metric)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting metric detail: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{metric_id}/profile-comparison")
async def get_metric_profile_comparison(
    metric_id: int,
    limit: int = 5,
    db: Session = Depends(get_database)
):
    """
    Get sample profiles for a metric comparison (group1 vs group2).
    Returns up to 'limit' profiles from each group with their fair and biased scores.
    """
    try:
        metric = db.query(BiasMetric).filter(BiasMetric.id == metric_id).first()
        if not metric:
            raise HTTPException(status_code=404, detail="Metric not found")
        
        # Filter profiles based on dimension and group names
        group1_profiles_query = db.query(StudentProfile)
        group2_profiles_query = db.query(StudentProfile)
        
        dimension = metric.dimension
        group1_name = metric.group1_name.lower()
        group2_name = metric.group2_name.lower()
        
        # Apply filters based on dimension
        if dimension == TestDimension.GEOGRAPHIC:
            # Urban vs Rural
            if "urban" in group1_name:
                group1_profiles_query = group1_profiles_query.filter(
                    StudentProfile.region.ilike("%urban%")
                )
            if "rural" in group1_name:
                group1_profiles_query = group1_profiles_query.filter(
                    StudentProfile.region.ilike("%rural%")
                )
            if "tier-1" in group1_name or "tier1" in group1_name:
                group1_profiles_query = group1_profiles_query.filter(
                    StudentProfile.region.ilike("%tier1%")
                )
            if "tier-2" in group1_name or "tier-3" in group1_name or "tier2" in group1_name or "tier3" in group1_name:
                group1_profiles_query = group1_profiles_query.filter(
                    or_(
                        StudentProfile.region.ilike("%tier2%"),
                        StudentProfile.region.ilike("%tier3%")
                    )
                )
            
            # Group 2 filters
            if "urban" in group2_name:
                group2_profiles_query = group2_profiles_query.filter(
                    StudentProfile.region.ilike("%urban%")
                )
            if "rural" in group2_name:
                group2_profiles_query = group2_profiles_query.filter(
                    StudentProfile.region.ilike("%rural%")
                )
            if "tier-1" in group2_name or "tier1" in group2_name:
                group2_profiles_query = group2_profiles_query.filter(
                    StudentProfile.region.ilike("%tier1%")
                )
            if "tier-2" in group2_name or "tier-3" in group2_name or "tier2" in group2_name or "tier3" in group2_name:
                group2_profiles_query = group2_profiles_query.filter(
                    or_(
                        StudentProfile.region.ilike("%tier2%"),
                        StudentProfile.region.ilike("%tier3%")
                    )
                )
        
        elif dimension == TestDimension.INCOME:
            # High Income vs Low Income
            if "high" in group1_name and "≥" in metric.group1_name:
                # Extract threshold (usually ₹20L)
                group1_profiles_query = group1_profiles_query.filter(
                    StudentProfile.family_income >= 2000000
                )
            if "low" in group1_name and "<" in metric.group1_name:
                group1_profiles_query = group1_profiles_query.filter(
                    StudentProfile.family_income < 1500000
                )
            
            if "high" in group2_name and "≥" in metric.group2_name:
                group2_profiles_query = group2_profiles_query.filter(
                    StudentProfile.family_income >= 2000000
                )
            if "low" in group2_name and "<" in metric.group2_name:
                group2_profiles_query = group2_profiles_query.filter(
                    StudentProfile.family_income < 1500000
                )
        
        elif dimension == TestDimension.CREDIT:
            # Good Credit vs Fair/Poor Credit
            if "good" in group1_name and "≥750" in metric.group1_name:
                group1_profiles_query = group1_profiles_query.filter(
                    StudentProfile.cibil_score >= 750
                )
            if "fair" in group1_name:
                group1_profiles_query = group1_profiles_query.filter(
                    and_(
                        StudentProfile.cibil_score >= 650,
                        StudentProfile.cibil_score < 750
                    )
                )
            if "poor" in group1_name and "<600" in metric.group1_name:
                group1_profiles_query = group1_profiles_query.filter(
                    StudentProfile.cibil_score < 600
                )
            
            if "good" in group2_name and "≥750" in metric.group2_name:
                group2_profiles_query = group2_profiles_query.filter(
                    StudentProfile.cibil_score >= 750
                )
            if "fair" in group2_name:
                group2_profiles_query = group2_profiles_query.filter(
                    and_(
                        StudentProfile.cibil_score >= 650,
                        StudentProfile.cibil_score < 750
                    )
                )
            if "poor" in group2_name and "<600" in metric.group2_name:
                group2_profiles_query = group2_profiles_query.filter(
                    StudentProfile.cibil_score < 600
                )
        
        elif dimension == TestDimension.EDGE_CASES:
            # Self-Employed vs Salaried
            if "self-employed" in group1_name:
                group1_profiles_query = group1_profiles_query.filter(
                    StudentProfile.employment_type.ilike("%self-employed%")
                )
            if "salaried" in group1_name:
                group1_profiles_query = group1_profiles_query.filter(
                    StudentProfile.employment_type.ilike("%salaried%")
                )
            if "single parent" in group1_name:
                group1_profiles_query = group1_profiles_query.filter(
                    StudentProfile.family_structure.ilike("%single_parent%")
                )
            if "nuclear" in group1_name:
                group1_profiles_query = group1_profiles_query.filter(
                    StudentProfile.family_structure.ilike("%nuclear%")
                )
            
            if "self-employed" in group2_name:
                group2_profiles_query = group2_profiles_query.filter(
                    StudentProfile.employment_type.ilike("%self-employed%")
                )
            if "salaried" in group2_name:
                group2_profiles_query = group2_profiles_query.filter(
                    StudentProfile.employment_type.ilike("%salaried%")
                )
            if "single parent" in group2_name:
                group2_profiles_query = group2_profiles_query.filter(
                    StudentProfile.family_structure.ilike("%single_parent%")
                )
            if "nuclear" in group2_name:
                group2_profiles_query = group2_profiles_query.filter(
                    StudentProfile.family_structure.ilike("%nuclear%")
                )
        
        # Get limited profiles from each group
        group1_profiles = group1_profiles_query.limit(limit).all()
        group2_profiles = group2_profiles_query.limit(limit).all()
        
        # Get scoring results for these profiles
        profile_ids_group1 = [p.id for p in group1_profiles]
        profile_ids_group2 = [p.id for p in group2_profiles]
        all_profile_ids = profile_ids_group1 + profile_ids_group2
        
        if not all_profile_ids:
            return {
                "metric": BiasMetricResponse.model_validate(metric),
                "group1_profiles": [],
                "group2_profiles": []
            }
        
        scoring_results = db.query(ScoringResult).filter(
            ScoringResult.profile_id.in_(all_profile_ids)
        ).all()
        
        # Organize scoring results by profile_id and type
        scores_by_profile = {}
        for score in scoring_results:
            if score.profile_id not in scores_by_profile:
                scores_by_profile[score.profile_id] = {}
            scores_by_profile[score.profile_id][score.scoring_type.value] = ScoringResultResponse.model_validate(score)
        
        # Build response
        def build_profile_response(profile: StudentProfile) -> Dict[str, Any]:
            profile_dict = StudentProfileResponse.model_validate(profile).model_dump()
            profile_scores = scores_by_profile.get(profile.id, {})
            return {
                "profile": profile_dict,
                "fair_score": profile_scores.get("fair"),
                "biased_score": profile_scores.get("biased")
            }
        
        return {
            "metric": BiasMetricResponse.model_validate(metric),
            "group1_profiles": [build_profile_response(p) for p in group1_profiles],
            "group2_profiles": [build_profile_response(p) for p in group2_profiles]
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting profile comparison: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/run/{test_run_id}", response_model=MetricsSummaryResponse)
async def get_metrics(
    test_run_id: str,
    db: Session = Depends(get_database)
):
    """
    Get metrics for a test run.
    """
    try:
        metrics = db.query(BiasMetric).filter(
            BiasMetric.test_run_id == test_run_id
        ).all()
        
        if not metrics:
            raise HTTPException(status_code=404, detail="Metrics not found")
        
        # Calculate summary
        overall_fairness_score = sum(m.overall_fairness_score for m in metrics) / len(metrics)
        critical_findings = len([m for m in metrics if m.severity.value == "critical"])
        high_findings = len([m for m in metrics if m.severity.value == "high"])
        medium_findings = len([m for m in metrics if m.severity.value == "medium"])
        low_findings = len([m for m in metrics if m.severity.value == "low"])
        
        return MetricsSummaryResponse(
            test_run_id=test_run_id,
            total_metrics=len(metrics),
            metrics=[BiasMetricResponse.model_validate(m) for m in metrics],
            overall_fairness_score=overall_fairness_score,
            critical_findings=critical_findings,
            high_findings=high_findings,
            medium_findings=medium_findings,
            low_findings=low_findings
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting metrics: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/", response_model=List[BiasMetricResponse])
async def list_metrics(
    dimension: Optional[TestDimension] = None,
    db: Session = Depends(get_database)
):
    """
    List all bias metrics, removing duplicates while keeping multiple edge case types.
    Order: Geographic, Income, Credit, Edge Cases (each sorted by ID within dimension).
    """
    try:
        from collections import defaultdict
        
        query = db.query(BiasMetric)
        if dimension:
            query = query.filter(BiasMetric.dimension == dimension)
        all_metrics = query.order_by(BiasMetric.created_at.desc()).all()
        
        # Track unique metrics by dimension and group names
        # For edge cases, we want to keep different types (e.g., Self-Employed vs Salaried, Single Parent vs Nuclear)
        # But remove duplicates of the same type
        seen_keys = set()
        unique_metrics = []
        
        # Process metrics in reverse order (most recent first) to keep latest when duplicates exist
        for metric in all_metrics:
            key = (metric.dimension, metric.group1_name, metric.group2_name)
            
            # For edge cases, allow multiple different edge case types
            # But remove duplicates of the same edge case type
            if metric.dimension == TestDimension.EDGE_CASES:
                if key not in seen_keys:
                    seen_keys.add(key)
                    unique_metrics.append(metric)
            else:
                # For other dimensions (Geographic, Income, Credit), keep only one entry per comparison
                if key not in seen_keys:
                    seen_keys.add(key)
                    unique_metrics.append(metric)
        
        # Sort by dimension order, then by id within each dimension
        dimension_order = {
            TestDimension.GEOGRAPHIC: 1,
            TestDimension.INCOME: 2,
            TestDimension.CREDIT: 3,
            TestDimension.EDGE_CASES: 4,
            TestDimension.GENDER: 5
        }
        
        unique_metrics.sort(key=lambda m: (
            dimension_order.get(m.dimension, 99),
            m.id
        ))
        
        return [BiasMetricResponse.model_validate(m) for m in unique_metrics]
    except Exception as e:
        logger.error(f"Error listing metrics: {e}", exc_info=True)
        # Return empty list instead of error
        return []
