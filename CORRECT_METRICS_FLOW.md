# ✅ Correct Metrics Flow: ML Model Bias

## 🎯 **You're Absolutely Right!**

The dashboard should show metrics from the **trained ML model's scoring** (initial bias), not just from mock profiles.

---

## ✅ **How It Actually Works (Already Correct!):**

### **Step 1: Train ML Model First**
```bash
python scripts/train_ml_model.py
```
This:
1. Imports real datasets
2. Trains ML model on real loan data (learns bias patterns)
3. Saves model to `backend/models/scoring_model.pkl`
4. Scores all profiles with:
   - **FAIR:** Deterministic (unbiased)
   - **BIASED:** ML Model (contains real-world bias)
5. Calculates **initial metrics** from ML model scores
6. Dashboard shows these **initial bias metrics**

### **Step 2: When Profiles Are Scored (via UI or API):**

The `ScoringService` automatically:
1. **Checks if ML model exists** (`scoring_model.pkl`)
2. **If ML model exists:**
   - FAIR scoring: Deterministic (unbiased)
   - **BIASED scoring: Uses ML Model** (`ml_model.predict_score()`)
3. **If ML model doesn't exist:**
   - FAIR: Deterministic
   - BIASED: Deterministic with penalties (fallback)

### **Step 3: Metrics Calculation:**

Metrics compare:
- **FAIR scores** (deterministic, unbiased)
- **BIASED scores** (from ML model if trained, showing real bias)

**Result:** Dashboard shows **bias present in the trained ML model** ✅

---

## ✅ **Key Code (Already Working Correctly):**

```python
# backend/app/services/scoring_service.py (lines 73-88)
ml_model = get_ml_model()
use_ml_model = ml_model is not None and ml_model.is_trained

if use_ml_model:
    if scoring_type == ScoringType.FAIR:
        result = DeterministicScoringEngine.calculate_fair_score(profile_dict)
    else:  # BIASED
        # ✅ Uses trained ML model for biased scoring!
        result = ml_model.predict_score(profile_dict, apply_bias=True)
```

---

## 🎯 **Correct Workflow:**

1. **First:** Train ML model (`python scripts/train_ml_model.py`)
   - Creates `scoring_model.pkl`
   - Scores profiles and calculates initial metrics

2. **Then:** Dashboard shows metrics from ML model scores
   - These represent **initial bias** in the trained model
   - Metrics persist until mitigation

3. **After Mitigation:** 
   - New scoring with improved prompts/model
   - New metrics calculated
   - Dashboard shows **improved metrics**

---

## ✅ **Summary:**

**The system is already correct!** ✅

- When ML model is trained, biased scoring uses the ML model
- Metrics are calculated from ML model scores
- Dashboard shows initial ML model bias metrics
- After mitigation, metrics update to show improvement

**The metrics shown ARE from the trained ML model** (if it's trained first). If metrics show 0, it's because:
1. ML model hasn't been trained yet, OR
2. Profiles haven't been scored yet, OR  
3. Metrics haven't been calculated yet

**Make sure to run `train_ml_model.py` first** to train the ML model and get initial bias metrics!
