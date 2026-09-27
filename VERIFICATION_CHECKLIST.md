# System Verification Checklist ✅

## Quick Status Check

Run these commands to verify everything is working:

### 1. Check Database ✅
```cmd
cd backend
venv\Scripts\activate
python scripts\check_data.py
```
**Expected Output:**
- Profiles: 2000
- Test Runs: 1 (completed)
- Scoring Results: 4000
- Bias Metrics: 6

### 2. Check Backend Server
Open: **http://localhost:8000/health**
**Expected:** `{"status":"healthy"}`

Or check API docs: **http://localhost:8000/docs**
**Expected:** FastAPI Swagger documentation

### 3. Check Dashboard API
Open: **http://localhost:8000/api/v1/dashboard**
**Expected:** JSON response with:
- `kpi_metrics` (approval_parity, interest_gap, collateral_gap, fairness_score)
- `top_findings` (array of bias findings)
- `heatmap_data` (bias counts by dimension and severity)
- `test_run_id`: "TEST_20251218_175808"

### 4. Check Frontend
Open: **http://localhost:3000/dashboard**
**Expected:**
- ✅ 4 KPI cards with values
- ✅ Bias heatmap showing dimensions
- ✅ Top findings list
- ✅ No "No test data available" message

---

## Current System Status

### ✅ Working Components
1. **Database**: All data loaded correctly
   - 2000 profiles from your datasets
   - ML model scoring results
   - Bias metrics calculated

2. **ML Model**: Trained and functional
   - Random Forest Classifier
   - 74.8% accuracy
   - Handling edge cases properly

3. **Dashboard**: Displaying real data
   - KPIs: Approval Parity, Interest Gap, Collateral Gap, Fairness Score (71.5/100)
   - Heatmap: Bias visualization
   - Top Findings: Critical issues highlighted

### 🔄 To Keep Running
- **Backend Server**: Port 8000 (must be running for dashboard to work)
- **Frontend Server**: Port 3000 (serves the web interface)

---

## If Something Isn't Working

### Dashboard shows "No test data available"
1. Check backend is running: http://localhost:8000/health
2. Hard refresh browser: Ctrl+F5
3. Check browser console for errors (F12)

### Backend won't start
1. Navigate to `backend` folder
2. Activate venv: `venv\Scripts\activate`
3. Check port 8000 is free: `netstat -ano | findstr :8000`
4. Start server: `python -m uvicorn app.main:app --reload --port 8000 --host 0.0.0.0`

### Frontend won't start
1. Navigate to `frontend` folder
2. Check `node_modules` exists (if not: `npm install`)
3. Check port 3000 is free: `netstat -ano | findstr :3000`
4. Start server: `npm run dev`

---

## Expected Dashboard Values

Based on your trained model:

- **Approval Parity**: ~0.71 (71% - below target of 95%)
- **Interest Gap**: ~2.5% (above target of 0.5%)
- **Collateral Gap**: ~15% (above target of 10%)
- **Fairness Score**: 71.5/100 (below target of 85)

These values indicate **bias is present** (which is expected for demonstration purposes).

