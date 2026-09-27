#!/usr/bin/env python3
"""
Check what the dashboard API is returning.
"""

import sys
import io
import requests
import json

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

try:
    response = requests.get("http://localhost:8000/api/v1/dashboard")
    if response.status_code == 200:
        data = response.json()
        print("\n=== DASHBOARD API RESPONSE ===\n")
        print(json.dumps(data, indent=2))
        print("\n=== KPI METRICS ===\n")
        kpi = data.get('kpi_metrics', {})
        print(f"Approval Parity: {kpi.get('approval_parity', 0)}")
        print(f"Interest Gap: {kpi.get('interest_gap', 0)}")
        print(f"Collateral Gap: {kpi.get('collateral_gap', 0)}")
        print(f"Fairness Score: {kpi.get('fairness_score', 0)}")
        print(f"\nTest Run ID: {data.get('test_run_id', 'N/A')}")
    else:
        print(f"Error: Status code {response.status_code}")
        print(response.text)
except requests.exceptions.ConnectionError:
    print("ERROR: Cannot connect to backend. Is it running on http://localhost:8000?")
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()

