# 🔧 Fix Dashboard Showing 0 Metrics

## 🔍 **Problem Identified**

You have **150 profiles** in the database, but:
- ❌ **0 Scoring Results** 
- ❌ **0 Bias Metrics**

This means the profiles were generated **before** the automatic scoring feature was added, so they were never scored.

---

## ✅ **Quick Fix**

### **Run this script to score existing profiles:**

```bash
cd backend
venv\Scripts\activate
python scripts\score_existing_profiles.py
```

This will:
1. ✅ Score all 150 profiles with FAIR model
2. ✅ Score all 150 profiles with BIASED model
3. ✅ Calculate bias metrics for all dimensions
4. ✅ Make metrics visible on dashboard

---

## 🎯 **After Running the Script**

1. **Wait for completion** (takes ~30-60 seconds)
2. **Refresh the dashboard** in your browser
3. **Metrics should now appear!** ✅

---

## 📊 **Expected Result**

After running the script, you should see:
- ✅ Approval Parity values (not 0.00)
- ✅ Interest Gap values (not 0.00%)
- ✅ Collateral Gap values (not 0.0%)
- ✅ Fairness Score values (not 0.0)
- ✅ Bias Heatmap with data
- ✅ Top Findings with bias issues

---

## 🚀 **For Future Profile Generation**

After you restart the backend (which you've already done), **new profiles will automatically be scored** and metrics will be calculated. But for existing profiles, you need to run this script once.

**Run the script now to fix the dashboard!** 🎯
