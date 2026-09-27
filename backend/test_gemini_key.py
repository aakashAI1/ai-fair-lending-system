#!/usr/bin/env python3
"""
Test script to verify Gemini API key works.
"""

import os
import sys

# Provide GEMINI_API_KEY in the environment before running this check.
if not os.environ.get("GEMINI_API_KEY"):
    print("GEMINI_API_KEY is not set; skipping Gemini credential check.")
    sys.exit(2)
os.environ["GEMINI_MODEL"] = "gemini-2.0-flash"

# Try to import and test
try:
    import google.generativeai as genai
    
    print("✓ google.generativeai imported successfully")
    
    # Configure with API key
    genai.configure(api_key=os.environ["GEMINI_API_KEY"])
    print("✓ API key configured")
    
    # Try to list models (this will verify the key works)
    try:
        models = list(genai.list_models())
        print(f"✓ API key is valid! Found {len(models)} available models")
        
        # Try to generate a simple response
        model = genai.GenerativeModel("gemini-2.0-flash")
        print("✓ Model initialized")
        
        response = model.generate_content("Say 'Hello, Gemini API is working!' in one sentence.")
        print(f"✓ Test response received: {response.text}")
        
        print("\n🎉 SUCCESS: Gemini API key is working correctly!")
        sys.exit(0)
        
    except Exception as e:
        print(f"✗ Error testing API: {str(e)}")
        print(f"  Error type: {type(e).__name__}")
        sys.exit(1)
        
except ImportError:
    print("✗ google.generativeai not installed")
    print("  Install with: pip install google-generativeai")
    sys.exit(1)
except Exception as e:
    print(f"✗ Unexpected error: {str(e)}")
    print(f"  Error type: {type(e).__name__}")
    sys.exit(1)
