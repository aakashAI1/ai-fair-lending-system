# 🔴 URGENT: FIX DELHI PROBLEM - STEP BY STEP

## ✅ **The Problem**
Your database still has **OLD profiles** with "Delhi" hardcoded. The fix is in the code, but you need to **clear old data** and **regenerate**.

---

## 🚀 **SOLUTION - Do These Steps NOW:**

### **Step 1: Clear ALL Old Profiles**

Open **PowerShell** or **Command Prompt** and run:

```cmd
cd "C:\Users\Aayush Sharma\OneDrive\Desktop\hitl-ai-fair-lending-validation\backend"
venv\Scripts\activate
python scripts\clear_all_profiles.py
```

This will **DELETE all old profiles** with "Delhi".

---

### **Step 2: Regenerate Profiles with Correct States**

**Option A: Using Training Script (RECOMMENDED)**
```cmd
python scripts\train_ml_model.py
```

This will:
- ✅ Import datasets
- ✅ Use research-based state distribution
- ✅ Generate diverse states (Maharashtra, Kerala, Tamil Nadu, etc.)
- ✅ Train ML model
- ✅ Score profiles

**Option B: Using UI "Generate Profiles" Button**
1. Go to http://localhost:3000/profiles
2. Click "Generate Profiles"
3. Enter count (e.g., 50-100)
4. Click Generate

---

### **Step 3: Refresh Frontend**

1. **Hard refresh** your browser: `Ctrl + Shift + R` (Windows) or `Cmd + Shift + R` (Mac)
2. Go to Profiles page
3. You should now see **diverse states**!

---

## ✅ **What You Should See After Fix**

- ✅ **~57% from Southern states**: Maharashtra, Kerala, Tamil Nadu, Karnataka, Andhra Pradesh, Telangana
- ✅ **~16% from Northern states**: Uttar Pradesh, Delhi (~3-4%), Punjab, Haryana
- ✅ **~12% from Western states**: Gujarat, Rajasthan, Madhya Pradesh
- ✅ **~10% from Eastern states**: West Bengal, Bihar, Odisha, Jharkhand
- ✅ **~5% from Northeastern**: Assam, Tripura, Manipur

**NO MORE "DELHI EVERYWHERE"!**

---

## ⚠️ **IMPORTANT**

- ✅ The fix is **already in the code**
- ✅ You MUST **clear old data** first
- ✅ Then **regenerate** profiles
- ✅ Simply refreshing frontend won't work - old data is still in database!

---

**DO STEP 1 AND STEP 2 NOW!** 🚀
