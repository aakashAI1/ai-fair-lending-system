"""
Unit tests for GenAI service.
"""

import pytest
from unittest.mock import Mock, patch
from app.services.genai_service import GenAIService


@pytest.mark.asyncio
async def test_generate_profiles():
    """Test profile generation."""
    # Mock GenAI service
    with patch('app.services.genai_service.ChatOpenAI') as mock_openai:
        mock_model = Mock()
        mock_model.invoke.return_value = Mock(content='[{"profile_id": "PROF_001", "name": "Test", "postcode": "110001", "region": "urban_tier1", "state": "Delhi", "family_income": 1000000, "cibil_score": 750, "requested_loan_amount": 500000, "gpa": 7.5, "course": "BTech", "educational_background": "Engineering", "co_applicant": "parent", "employment_type": "salaried", "family_structure": "nuclear", "test_dimension": "geographic"}]')
        mock_openai.return_value = mock_model
        
        service = GenAIService()
        profiles = await service.generate_profiles(count=1, dimensions=['geographic'])
        
        assert len(profiles) == 1
        assert profiles[0]['profile_id'] == 'PROF_001'


@pytest.mark.asyncio
async def test_score_profile():
    """Test profile scoring."""
    # Mock GenAI service
    with patch('app.services.genai_service.ChatOpenAI') as mock_openai:
        mock_model = Mock()
        mock_model.invoke.return_value = Mock(content='{"score": 8.5, "approval_decision": "approve", "interest_rate": 11.0, "collateral_required": false, "reasoning": "Good profile"}')
        mock_openai.return_value = mock_model
        
        service = GenAIService()
        profile = {
            "profile_id": "PROF_001",
            "name": "Test",
            "family_income": 1000000,
            "cibil_score": 750,
            "gpa": 7.5  # Indian 10-point scale
        }
        result = await service.score_profile(profile, "fair", 500000)
        
        assert result['score'] == 8.5
        assert result['approval_decision'] == 'approve'







