# 📊 Dashboard Metrics: ML Model vs Mock Profiles

## ✅ **Correct Understanding**

You're absolutely right! The dashboard should show metrics from the **trained ML model**, not from mock profiles.

---

## 🎯 **Correct Flow:**

### **1. Training Phase (`train_ml_model.py`):**
```
Import Real Datasets 
    ↓
Train ML Model on Real Loan Data
    ↓
Score All Profiles:
    - FAIR: Deterministic (unbiased)
    - BIASED: ML Model (trained on real data, contains bias)
    ↓
Calculate Initial Metrics from ML Model Scores
    ↓
Dashboard Shows: Initial Bias Metrics (from trained ML model)
```

### **2. Dashboard Display:**
- Shows metrics calculated from **ML model's biased scoring**
- These represent the **initial bias state** of the trained model
- Metrics persist until mitigation

### **3. After Mitigation:**
- New scoring with improved model/prompts
- New metrics calculated showing improvement
- Dashboard updates to show improved metrics

---

## ⚠️ **Current Issue:**

When profiles are generated via UI:
- They should be scored with the **trained ML model** (if it exists)
- Metrics should be calculated from **ML model scores**
- Dashboard should show these **initial bias metrics**

**The system already does this correctly:**
- `ScoringService` checks if ML model exists
- If ML model exists, uses it for BIASED scoring
- Metrics are calculated from FAIR vs BIASED scores
- Dashboard displays these metrics

---

## ✅ **What's Already Working:**

1. **ML Model Scoring:**
   - When ML model is trained, `ScoringService` uses it for biased scoring
   - Falls back to deterministic only if ML model not available

2. **Metrics Calculation:**
   - Metrics are calculated from FAIR vs BIASED scoring results
   - If ML model was used for biased scoring, metrics reflect ML model bias

3. **Dashboard:**
   - Shows metrics from latest test run
   - Displays initial bias metrics until mitigation

---

## 🎯 **The Key Point:**

**Metrics = Comparison between FAIR scoring vs BIASED scoring**

- **FAIR:** Always deterministic (unbiased)
- **BIASED:** ML model if trained (contains real-world bias) OR deterministic with penalties

**Dashboard metrics show the bias present in the BIASED scoring method** (which should be the trained ML model if it exists).

---

## ✅ **Summary:**

The architecture is correct:
- ML model is used for biased scoring (if trained)
- Metrics compare fair vs biased
- Dashboard shows initial ML model bias metrics
- After mitigation, new metrics show improvement

**The system already works this way!** The dashboard will show ML model metrics as long as:
1. ML model is trained (`python scripts/train_ml_model.py`)
2. Profiles are scored with the ML model
3. Metrics are calculated from these scores
