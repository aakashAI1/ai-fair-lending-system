#!/usr/bin/env python3
"""
Comprehensive setup script to generate showcase-ready data.
This script will:
1. Generate realistic student profiles
2. Score them with fair and biased models
3. Calculate bias metrics
4. Create sample feedback
5. Ensure dashboard is ready for showcase
"""

import sys
import os
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

import io
import subprocess

if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

def main():
    print("=" * 70)
    print("FAIR LENDING AI VALIDATION - SHOWCASE DATA SETUP")
    print("=" * 70)
    print("\nThis script will generate realistic data for showcasing the system.")
    print("It will create:")
    print("  - 500 realistic student profiles")
    print("  - Fair and biased scoring results")
    print("  - Comprehensive bias metrics")
    print("  - Sample human feedback")
    print("\nThis may take a few minutes...\n")
    
    try:
        # Import and run the data generation script
        from generate_realistic_data import populate_database_realistic
        
        # Generate 500 profiles for good statistical significance
        num_profiles = 500
        print(f"Generating {num_profiles} profiles...")
        populate_database_realistic(num_profiles)
        
        print("\n" + "=" * 70)
        print("✅ SETUP COMPLETE!")
        print("=" * 70)
        print("\nYour dashboard is now ready for showcase!")
        print("\nNext steps:")
        print("  1. Make sure backend is running: cd backend && python -m uvicorn app.main:app --reload")
        print("  2. Make sure frontend is running: cd frontend && npm run dev")
        print("  3. Open http://localhost:3000/dashboard in your browser")
        print("\nThe dashboard will show:")
        print("  - Real-time bias metrics")
        print("  - KPI cards with accuracy indicators")
        print("  - Bias heatmap across dimensions")
        print("  - Top findings with severity levels")
        print("=" * 70 + "\n")
        
    except Exception as e:
        print(f"\n❌ Error during setup: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()

