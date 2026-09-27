# Retrain ML Model - Instructions

## The Problem
The ML model was trained on your datasets, but a bug in the prediction code caused all loans to be rejected (0% approval rate). This is now fixed.

## Solution: Retrain the Model

You need to retrain the model to regenerate the scoring results with the fix applied.

### Step 1: Clean the Database (Optional but Recommended)

If you want fresh results, you can clear the old scoring results and metrics:

```cmd
cd backend
venv\Scripts\activate
python -c "from app.database import SessionLocal; from app.models import ScoringResult, BiasMetric, TestRun; db = SessionLocal(); db.query(ScoringResult).delete(); db.query(BiasMetric).delete(); db.query(TestRun).delete(); db.commit(); print('Database cleaned')"
```

**OR** just retrain - the script will overwrite the old test run.

### Step 2: Retrain the Model

Run the training script:

```cmd
cd backend
venv\Scripts\activate
python scripts\train_ml_model.py
```

This will:
1. ✅ Load your datasets (fair_lending_audit_realistic_500.csv and super_loan_dataset_v3_no_interview.csv)
2. ✅ Train the ML model (with the bug fix applied)
3. ✅ Score all 2000 profiles with the corrected model
4. ✅ Calculate bias metrics
5. ✅ Save everything to the database

### Step 3: Verify Results

Check that approvals are now happening:

```cmd
python scripts\check_metrics_values.py
```

You should see:
- ✅ Fair approvals: Some percentage (not 0.10%)
- ✅ Biased approvals: Some percentage (not 0.00%)
- ✅ Metrics with non-zero values for Approval Parity, Interest Gap, Collateral Gap

### Step 4: Refresh Dashboard

1. Make sure backend is running: http://localhost:8000/health
2. Refresh your dashboard: http://localhost:3000/dashboard
3. You should now see real metrics instead of zeros!

---

## What Changed?

**Before (Bug):**
- Model predicted approval probability incorrectly
- All loans rejected → 0% approval rate
- All metrics showed 0.0 (can't compare 0% vs 0%)

**After (Fixed):**
- Model correctly extracts approval probability from predict_proba
- Loans are approved based on model prediction
- Metrics show real bias differences

---

## No API Key Needed!

The ML model runs **locally** using scikit-learn. No API keys required. API keys are only needed for GenAI features (which we're not using for scoring).

