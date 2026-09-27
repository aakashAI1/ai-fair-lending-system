"""
Test script to verify GenAI API (Google Gemini) is working correctly.
This will check if the API key is configured and if API calls succeed.
"""

import sys
from pathlib import Path
import logging

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.config import settings
from app.services.genai_service import genai_service
import asyncio

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

async def test_genai_api():
    """Test GenAI API with a simple profile generation."""
    
    print("\n" + "="*60)
    print("GenAI API Test (Google Gemini)")
    print("="*60)
    
    # Check API key configuration
    print("\n1. Checking API Key Configuration...")
    api_key_configured = (
        settings.GEMINI_API_KEY 
        and settings.GEMINI_API_KEY != "your-gemini-api-key-here"
        and len(settings.GEMINI_API_KEY) > 0
    )
    
    if api_key_configured:
        print(f"   [OK] API Key is configured")
        print(f"   [OK] API Key: {settings.GEMINI_API_KEY[:20]}...")
        print(f"   [OK] Model: {settings.GEMINI_MODEL}")
    else:
        print(f"   [ERROR] API Key is NOT configured")
        print(f"   -> Check backend/.env file for GEMINI_API_KEY")
        print(f"   -> Current value: {settings.GEMINI_API_KEY}")
        return False
    
    # Check GenAI service initialization
    print("\n2. Checking GenAI Service Initialization...")
    try:
        provider = genai_service.provider
        model_initialized = genai_service.model is not None
        
        print(f"   [OK] Provider: {provider}")
        
        if model_initialized:
            print(f"   [OK] Model is initialized")
        else:
            print(f"   [ERROR] Model is NOT initialized (will use mock responses)")
            print(f"   -> Check if google-generativeai package is installed")
            print(f"   -> Run: pip install google-generativeai")
            return False
            
    except Exception as e:
        print(f"   [ERROR] Error: {e}")
        return False
    
    # Test actual API call
    print("\n3. Testing API Call (Generating 1 Profile)...")
    try:
        print("   -> Calling Gemini API...")
        profiles = await genai_service.generate_profiles(
            count=1,
            dimensions=["geographic"]
        )
        
        if profiles and len(profiles) > 0:
            print(f"   [OK] SUCCESS! Generated {len(profiles)} profile(s)")
            print(f"   [OK] Profile ID: {profiles[0].get('profile_id', 'N/A')}")
            print(f"   [OK] Name: {profiles[0].get('name', 'N/A')}")
            print(f"   [OK] Region: {profiles[0].get('region', 'N/A')}")
            print(f"   [OK] GPA: {profiles[0].get('gpa', 'N/A')}")
            
            # Check if it's a real response or mock
            profile_id = profiles[0].get('profile_id', '')
            if len(profile_id) == 8 and all(c in '0123456789ABCDEFabcdef' for c in profile_id):
                # Real profiles have 8-character hex ID format
                print("\n   [WARNING] This appears to be a MOCK response")
                print("   -> Real API calls may have failed")
                print("   -> Check backend logs for GenAI errors")
                return False
            else:
                print("\n   [OK] This appears to be a REAL API response!")
                return True
        else:
            print(f"   [ERROR] No profiles generated")
            return False
            
    except Exception as e:
        print(f"   [ERROR] API Call Failed: {e}")
        logger.exception("Full error details:")
        return False

def main():
    """Main test function."""
    try:
        result = asyncio.run(test_genai_api())
        
        print("\n" + "="*60)
        if result:
            print("[SUCCESS] GenAI API is WORKING correctly!")
            print("="*60)
            sys.exit(0)
        else:
            print("[FAILED] GenAI API is NOT working (using mock responses)")
            print("="*60)
            print("\nTroubleshooting:")
            print("1. Check backend/.env file has GEMINI_API_KEY set")
            print("2. Verify API key is valid: https://aistudio.google.com/app/apikey")
            print("3. Install package: pip install google-generativeai")
            print("4. Check backend logs for detailed error messages")
            sys.exit(1)
            
    except KeyboardInterrupt:
        print("\n\nTest interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n[ERROR] Unexpected error: {e}")
        logger.exception("Full error details:")
        sys.exit(1)

if __name__ == "__main__":
    main()
