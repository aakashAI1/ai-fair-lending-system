# ✅ Dashboard: Always Show Metrics (Never 0)

## 🎯 **Fixed:**

The dashboard now **always shows the latest metrics** from the ML model training, even if you generate new profiles.

---

## ✅ **How It Works:**

### **Before Fix:**
- Dashboard only looked for metrics from the **current test run**
- If you generated new profiles, new test run created → no metrics → showed 0

### **After Fix:**
- Dashboard first looks for metrics from current test run
- **If not found, finds latest metrics from ANY test run**
- Always shows metrics (from ML model training), never 0

---

## 🔄 **ML Model Training: ONE-TIME**

### **Answer: NO, you don't train every time!**

**Training is ONE-TIME setup:**

1. **Train Once:**
   ```bash
   python scripts\train_ml_model.py
   ```
   - Trains model on datasets
   - **Saves to:** `backend/models/scoring_model.pkl` (persists on disk)
   - Creates initial metrics

2. **Model Persists:**
   - Model file saved to disk
   - Loaded automatically when needed
   - **Reused for all scoring operations**

3. **No Retraining Needed:**
   - Model is loaded from disk for every scoring
   - Training only needed once (or when you want to retrain)

---

## 📊 **Dashboard Behavior:**

### **Scenario 1: ML Model Trained**
1. Run `train_ml_model.py` → Creates metrics
2. Dashboard shows metrics from ML model ✅
3. Generate new profiles → Dashboard **still shows ML model metrics** ✅
4. Metrics persist until mitigation

### **Scenario 2: No ML Model Trained**
1. Generate profiles → No metrics yet
2. Auto-scoring triggers → Creates metrics
3. Dashboard shows metrics ✅

---

## 🎯 **Key Points:**

✅ **ML Model Training:** ONE-TIME (model saved to disk)  
✅ **Metrics Persist:** Always shown (from latest test run)  
✅ **Never Shows 0:** Falls back to latest available metrics  
✅ **After Mitigation:** New metrics replace old ones  

**The dashboard will always show metrics now!** 🎯
