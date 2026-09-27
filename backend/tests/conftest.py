"""
Pytest configuration and fixtures.
"""

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database import Base, get_db
from app.models import StudentProfile, ScoringResult, BiasMetric


@pytest.fixture
def db_session():
    """Create a test database session."""
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    SessionLocal = sessionmaker(bind=engine)
    session = SessionLocal()
    yield session
    session.close()
    Base.metadata.drop_all(engine)


@pytest.fixture
def test_profile(db_session):
    """Create a test profile."""
    profile = StudentProfile(
        profile_id="TEST_001",
        name="Test Student",
        postcode="110001",
        region="urban_tier1",
        state="Delhi",
        family_income=1000000,
        cibil_score=750,
        requested_loan_amount=500000,
        gpa=7.5,  # Indian 10-point scale
        course="BTech",
        educational_background="Engineering",
        co_applicant="parent",
        employment_type="salaried",
        family_structure="nuclear",
        test_dimension="geographic"
    )
    db_session.add(profile)
    db_session.commit()
    return profile







