"""
Pydantic schemas for request/response validation.
"""

from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List, Dict, Any, Literal
from datetime import datetime
from enum import Enum

from app.models import TestDimension, ScoringType, SeverityLevel


# ==================== Profile Schemas ====================

class StudentProfileCreate(BaseModel):
    """Schema for creating a student profile."""
    profile_id: str
    name: str
    postcode: str
    region: str
    state: str
    family_income: int = Field(..., ge=0, description="Family income in rupees")
    cibil_score: int = Field(..., ge=300, le=900, description="CIBIL score (300-900)")
    requested_loan_amount: int = Field(..., ge=500000, le=5000000, description="Loan amount in rupees")
    gpa: float = Field(..., ge=0.0, le=10.0, description="GPA (0.0-10.0, Indian 10-point scale)")
    course: str
    educational_background: str
    college_tier: Optional[str] = Field(None, description="College tier: tier1, tier2, or tier3")
    university_name: Optional[str] = Field(None, description="Name of the college/university")
    co_applicant: Optional[str] = None
    employment_type: str
    family_structure: str
    test_dimension: TestDimension


class StudentProfileResponse(BaseModel):
    """Schema for student profile response."""
    id: int
    profile_id: str
    name: str
    postcode: str
    region: str
    state: str
    family_income: int
    cibil_score: int
    requested_loan_amount: int
    gpa: float
    course: str
    educational_background: str
    college_tier: Optional[str] = None
    university_name: Optional[str] = None
    co_applicant: Optional[str]
    employment_type: str
    family_structure: str
    test_dimension: TestDimension
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)


# ==================== Scoring Schemas ====================

class ScoringRequest(BaseModel):
    """Schema for scoring request."""
    profile_ids: Optional[List[int]] = None  # If None, score all profiles
    scoring_type: ScoringType
    batch_size: int = Field(default=100, ge=1, le=1000)


class ScoringResultResponse(BaseModel):
    """Schema for scoring result response."""
    id: int
    profile_id: int
    scoring_type: ScoringType
    score: float = Field(..., ge=1.0, le=10.0)
    approval_decision: str
    interest_rate: float = Field(..., ge=8.0, le=15.0)
    collateral_required: bool
    reasoning: Optional[str]
    prompt_version: Optional[str]
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)


class ScoringBatchResponse(BaseModel):
    """Schema for batch scoring response."""
    total_scored: int
    successful: int
    failed: int
    results: List[ScoringResultResponse]
    errors: List[Dict[str, Any]]


# ==================== Metrics Schemas ====================

class BiasMetricResponse(BaseModel):
    """Schema for bias metric response."""
    id: int
    test_run_id: str
    dimension: TestDimension
    approval_parity: float
    interest_rate_disparity: float
    collateral_gap: float
    edge_case_coverage: float
    overall_fairness_score: float
    p_value: Optional[float]
    t_statistic: Optional[float]
    is_statistically_significant: bool
    confidence_interval_lower: Optional[float]
    confidence_interval_upper: Optional[float]
    severity: SeverityLevel
    group1_name: str
    group2_name: str
    group1_approval_rate: float
    group2_approval_rate: float
    group1_interest_rate: float
    group2_interest_rate: float
    group1_collateral_pct: float
    group2_collateral_pct: float
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)


class MetricsCalculationRequest(BaseModel):
    """Schema for metrics calculation request."""
    test_run_id: str
    dimensions: List[TestDimension] = Field(default_factory=lambda: list(TestDimension))


class MetricsSummaryResponse(BaseModel):
    """Schema for metrics summary response."""
    test_run_id: str
    total_metrics: int
    metrics: List[BiasMetricResponse]
    overall_fairness_score: float
    critical_findings: int
    high_findings: int
    medium_findings: int
    low_findings: int


# ==================== Feedback Schemas ====================

class HumanFeedbackCreate(BaseModel):
    """Schema for creating human feedback."""
    bias_metric_id: int
    is_discriminatory: Literal["yes", "no", "partially"]
    root_cause_analysis: Optional[str] = None
    severity_rating: int = Field(..., ge=1, le=5)
    suggested_mitigation: Optional[str] = None
    annotator_name: Optional[str] = None
    annotator_role: Optional[str] = None


class HumanFeedbackResponse(BaseModel):
    """Schema for human feedback response."""
    id: int
    bias_metric_id: int
    is_discriminatory: str
    root_cause_analysis: Optional[str]
    severity_rating: int
    suggested_mitigation: Optional[str]
    annotator_name: Optional[str]
    annotator_role: Optional[str]
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)


# ==================== Mitigation Schemas ====================

class MitigationRequest(BaseModel):
    """Schema for mitigation request."""
    test_run_id: str
    feedback_ids: List[int]
    max_iterations: int = Field(default=3, ge=1, le=10)
    target_fairness_score: float = Field(default=85.0, ge=0.0, le=100.0)


class MitigationResultResponse(BaseModel):
    """Schema for mitigation result response."""
    id: int
    mitigation_run_id: str
    iteration_number: int
    prompt_version: str
    prompt_text: str
    prompt_changes: Optional[str]
    before_fairness_score: Optional[float]
    after_fairness_score: float
    improvement_percentage: float
    target_achieved: bool
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)


class MitigationComparisonResponse(BaseModel):
    """Schema for before/after mitigation comparison."""
    mitigation_run_id: str
    iterations: List[MitigationResultResponse]
    initial_fairness_score: float
    final_fairness_score: float
    total_improvement: float
    target_achieved: bool


# ==================== Profile Generation Schemas ====================

class ProfileGenerationRequest(BaseModel):
    """Schema for profile generation request."""
    count: int = Field(default=3100, ge=1, le=10000)
    dimensions: List[TestDimension] = Field(default_factory=lambda: list(TestDimension))
    batch_size: int = Field(default=100, ge=1, le=1000)


class ProfileGenerationResponse(BaseModel):
    """Schema for profile generation response."""
    test_run_id: str
    total_generated: int
    profiles: List[StudentProfileResponse]
    status: str
    progress_percentage: float


# ==================== Dashboard Schemas ====================

class KPIMetrics(BaseModel):
    """Schema for KPI metrics."""
    approval_parity: float
    interest_gap: float
    collateral_gap: float
    fairness_score: float
    severity: SeverityLevel


class TopFinding(BaseModel):
    """Schema for top finding."""
    id: int
    dimension: TestDimension
    description: str
    severity: SeverityLevel
    metric_value: float
    group1_name: str
    group2_name: str
    group1_value: float
    group2_value: float


class DashboardResponse(BaseModel):
    """Schema for dashboard response."""
    kpi_metrics: KPIMetrics
    top_findings: List[TopFinding]
    heatmap_data: Dict[str, Dict[str, float]]
    test_run_id: str
    last_updated: datetime


# ==================== WebSocket Schemas ====================

class WebSocketMessage(BaseModel):
    """Schema for WebSocket messages."""
    type: str
    data: Dict[str, Any]
    timestamp: datetime = Field(default_factory=datetime.now)


class ProgressUpdate(BaseModel):
    """Schema for progress update."""
    test_run_id: str
    status: str
    progress_percentage: float
    current_step: str
    total_profiles: int
    processed_profiles: int


# ==================== Authentication Schemas ====================

class LoginRequest(BaseModel):
    """Schema for login request."""
    employee_id: str = Field(..., min_length=1, description="Employee ID")
    password: str = Field(..., min_length=1, description="Password")


class TokenResponse(BaseModel):
    """Schema for token response."""
    access_token: str
    token_type: str = "bearer"
    user: Dict[str, Any]


class UserResponse(BaseModel):
    """Schema for user response."""
    id: int
    employee_id: str
    full_name: str
    email: Optional[str] = None
    role: str
    is_active: bool
    
    model_config = ConfigDict(from_attributes=True)







