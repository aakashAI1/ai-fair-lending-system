#!/usr/bin/env python3
"""
Setup script to create .env file with Gemini API key.
"""

import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

import os
from pathlib import Path

# Provide GEMINI_API_KEY in the environment before running this helper.
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")

# Path to .env file
env_file = Path(__file__).parent / ".env"

# Create .env content
env_content = f"""# Gemini API Configuration
GEMINI_API_KEY={GEMINI_API_KEY}
GEMINI_MODEL=gemini-2.0-flash

# Application Settings
DEBUG=True
ENVIRONMENT=development

# Database (SQLite for development)
DATABASE_URL=sqlite:///./fairlending.db

# CORS Origins (for frontend)
CORS_ORIGINS=["http://localhost:3000", "http://localhost:3001"]
"""

# Write .env file
try:
    with open(env_file, 'w', encoding='utf-8') as f:
        f.write(env_content)
    print(f"[OK] Created .env file at: {env_file}")
    print("[OK] Gemini API key configured." if GEMINI_API_KEY else "[INFO] No Gemini API key set; mock responses will be used.")
except Exception as e:
    print(f"[ERROR] Error creating .env file: {e}")
    print(f"\nPlease create .env file manually with this content:")
    print("\n" + "="*60)
    print(env_content)
    print("="*60)
