# 🚀 Complete Setup - One-Click Start

## ✅ **New Batch File Created!**

Created **`run-complete-setup.bat`** that runs everything at once!

---

## 🎯 **What It Does:**

1. **Checks ML Model:**
   - If model exists → Skips training (saves time)
   - If model doesn't exist → Trains ML model first

2. **Starts Backend Server:**
   - Opens in new window
   - Runs on `http://localhost:8000`

3. **Starts Frontend Server:**
   - Opens in new window
   - Runs on `http://localhost:3000`

---

## 📋 **How to Use:**

### **Option 1: Double-Click**
1. Double-click **`run-complete-setup.bat`**
2. Wait for all windows to open
3. Open browser: `http://localhost:3000/dashboard`

### **Option 2: Command Line**
```cmd
run-complete-setup.bat
```

---

## 🪟 **What You'll See:**

**Three Windows Will Open:**

1. **Window 1: Backend Server**
   - Shows: `Uvicorn running on http://0.0.0.0:8000`
   - **Keep this open!**

2. **Window 2: Frontend Server**
   - Shows: `Ready - started server on 0.0.0.0:3000`
   - **Keep this open!**

3. **Window 3: Setup Script (This One)**
   - Shows setup progress
   - Can be closed after setup completes

---

## ⚡ **Smart Features:**

✅ **Skips Training if Model Exists:**
   - Checks for `backend/models/scoring_model.pkl`
   - Only trains if file doesn't exist
   - Saves time on subsequent runs

✅ **Automatic Virtual Environment:**
   - Activates venv automatically
   - No manual activation needed

✅ **Error Handling:**
   - Checks if venv exists
   - Handles training failures gracefully
   - Continues even if training fails

---

## 🔄 **First Time vs Subsequent Runs:**

### **First Time:**
- Trains ML model (~1-2 minutes)
- Starts backend
- Starts frontend
- Total: ~2-3 minutes

### **Subsequent Runs:**
- Skips training (model exists)
- Starts backend
- Starts frontend
- Total: ~10 seconds

---

## 🎯 **Quick Access:**

After running the batch file, open:
- **Dashboard:** http://localhost:3000/dashboard
- **API Docs:** http://localhost:8000/docs
- **Backend Health:** http://localhost:8000/health

---

## ✅ **That's It!**

Just double-click `run-complete-setup.bat` and everything starts automatically! 🚀
