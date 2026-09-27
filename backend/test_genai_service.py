#!/usr/bin/env python3
"""
Test script to verify GenAI service works with the new Gemini API key.
"""

import os
import sys
import asyncio

# Provide GEMINI_API_KEY in the environment before running this check.
os.environ["GEMINI_MODEL"] = "gemini-2.0-flash"
os.environ["DATABASE_URL"] = "sqlite:///./test_fairlending.db"

# Now import the service
from app.services.genai_service import GenAIService

async def test_service():
    print("Testing GenAI Service with Gemini API key...")
    print("=" * 60)

    try:
        service = GenAIService()
        print(f"✓ GenAI Service initialized")
        print(f"✓ Provider: {service.provider}")
        
        if service.provider == "mock":
            print("⚠ Warning: Service is using mock provider")
            print("  This means the API key wasn't detected properly")
            return False
        
        # Test profile generation
        print("\n📝 Testing profile generation...")
        from app.models import TestDimension
        dimensions = [TestDimension.GENDER.value, TestDimension.GEOGRAPHIC.value]
        profiles = await service.generate_profiles(count=2, dimensions=dimensions)
        print(f"✓ Generated {len(profiles)} profiles")
        if profiles:
            print(f"  Sample profile keys: {list(profiles[0].keys())}")
        
        # Test scoring
        print("\n📊 Testing scoring...")
        test_profile = {
            "name": "Test Student",
            "age": 22,
            "gender": "Male",
            "caste": "General",
            "income": 500000,
            "credit_score": 750,
            "education_level": "Graduate",
            "course": "Engineering",
            "university": "IIT Delhi"
        }
        
        fair_score = await service.score_profile(test_profile, scoring_type="fair")
        print(f"✓ Fair scoring completed")
        print(f"  Approval: {fair_score.get('approved', 'N/A')}")
        print(f"  Interest Rate: {fair_score.get('interest_rate', 'N/A')}%")
        
        biased_score = await service.score_profile(test_profile, scoring_type="biased")
        print(f"✓ Biased scoring completed")
        print(f"  Approval: {biased_score.get('approved', 'N/A')}")
        print(f"  Interest Rate: {biased_score.get('interest_rate', 'N/A')}%")
        
        print("\n" + "=" * 60)
        print("🎉 SUCCESS: GenAI Service is working correctly with Gemini!")
        print("=" * 60)
        return True
        
    except Exception as e:
        print(f"\n✗ Error: {str(e)}")
        print(f"  Error type: {type(e).__name__}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = asyncio.run(test_service())
    sys.exit(0 if success else 1)
