# Why Dashboard Shows No Data - Quick Fix Guide 🔍

## Problem
Your backend and frontend are running correctly ✅, but the dashboard shows:
- Empty approval metrics
- No bias heatmap
- No top findings

**Reason:** The database is empty! You need to import data and train the ML model first.

---

## Solution: Import Data & Train Model (3 Steps)

### Step 1: Open a NEW Terminal Window
Keep your backend and frontend running in their windows. Open a **third terminal window**.

### Step 2: Navigate to Backend
```cmd
cd "C:\Users\Aayush Sharma\OneDrive\Desktop\hitl-ai-fair-lending-validation\backend"
venv\Scripts\activate
```

### Step 3: Run the Training Script
```cmd
python scripts\train_ml_model.py
```

**What this does:**
1. ✅ Imports student profiles from datasets
2. ✅ Trains the ML model
3. ✅ Scores all profiles (fair + biased)
4. ✅ Calculates bias metrics
5. ✅ Populates the database

**Wait time:** 1-2 minutes

---

## After Training Completes

1. **Refresh your browser** (http://localhost:3000/dashboard)
2. **You should now see:**
   - ✅ Approval metrics (KPIs)
   - ✅ Bias heatmap with data
   - ✅ Top findings list

---

## Quick Alternative (If Training Fails)

If the training script can't find datasets, you can generate synthetic profiles instead:

1. Go to: http://localhost:3000/profiles
2. Click "Generate Profiles with GenAI"
3. Enter count: `100`
4. Select dimensions: `Geographic`, `Income`, `Credit`
5. Click "Generate Profiles"
6. Wait for generation to complete
7. Then go to the dashboard - metrics should appear

---

## Verify Data Was Created

Check if data exists:
```cmd
cd backend
venv\Scripts\activate
python scripts\check_data.py
```

You should see counts for:
- StudentProfile records
- ScoringResult records  
- BiasMetric records
- TestRun records

---

## Still Not Working?

1. **Check backend logs** - look for errors
2. **Check browser console** (F12) - look for API errors
3. **Verify datasets exist:**
   - `backend/data/fair_lending_audit_realistic_500.csv`
   - `backend/data/super_loan_dataset_v3_no_interview.csv`

If datasets are missing, use the GenAI profile generation method above instead.
