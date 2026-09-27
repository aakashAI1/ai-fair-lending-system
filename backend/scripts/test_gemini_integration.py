#!/usr/bin/env python3
"""
Test that the Gemini API key is properly configured and working.
"""

import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

# Load environment variables from .env file
from dotenv import load_dotenv
load_dotenv(Path(__file__).parent.parent / '.env')

from app.services.genai_service import GenAIService
from app.config import settings
import asyncio

async def test_gemini():
    print("\n=== Testing Gemini API Integration ===\n")
    
    # Check if API key is set
    print(f"API Key configured: {settings.GEMINI_API_KEY is not None and settings.GEMINI_API_KEY != 'your-gemini-api-key-here'}")
    if settings.GEMINI_API_KEY:
        print(f"API Key: {settings.GEMINI_API_KEY[:20]}...")
    print(f"Model: {settings.GEMINI_MODEL}")
    print()
    
    # Initialize service
    try:
        service = GenAIService()
        print(f"✓ GenAI Service initialized")
        print(f"✓ Provider: {service.provider}")
        
        if service.provider == "mock":
            print("\n⚠ WARNING: Service is using mock provider!")
            print("   This means the API key wasn't detected properly")
            print("   Check that GEMINI_API_KEY is set in .env file")
            return False
        
        if service.provider != "gemini":
            print(f"\n⚠ Provider is '{service.provider}', expected 'gemini'")
            return False
        
        print("\n✓ Using Gemini API (not mock)")
        
        # Test a simple profile generation
        print("\n📝 Testing profile generation (this may take a few seconds)...")
        from app.models import TestDimension
        try:
            profiles = await service.generate_profiles(
                count=1,
                dimensions=[TestDimension.GEOGRAPHIC.value]
            )
            print(f"✓ Generated {len(profiles)} profile(s)")
            if profiles:
                profile = profiles[0]
                print(f"  Sample profile keys: {list(profile.keys())}")
                print(f"  Name: {profile.get('name', 'N/A')}")
                print(f"  Region: {profile.get('region', 'N/A')}")
                print(f"  State: {profile.get('state', 'N/A')}")
            print("\n✅ Gemini API integration is working correctly!")
            return True
        except Exception as e:
            print(f"\n❌ Error during profile generation: {e}")
            import traceback
            traceback.print_exc()
            return False
            
    except Exception as e:
        print(f"\n❌ Error initializing GenAI service: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    try:
        result = asyncio.run(test_gemini())
        sys.exit(0 if result else 1)
    except KeyboardInterrupt:
        print("\n\nTest interrupted by user")
        sys.exit(1)

