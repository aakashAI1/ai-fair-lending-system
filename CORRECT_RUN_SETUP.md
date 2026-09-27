# ✅ Correct Way to Run the Setup

## 🚀 **Option 1: One-Click Setup (Easiest!)**

**Just double-click:**
```
run-complete-setup.bat
```

This automatically:
1. ✅ Trains ML model (if not already trained)
2. ✅ Starts backend server
3. ✅ Starts frontend server
4. ✅ Opens everything in separate windows

**That's it!** Open browser: http://localhost:3000/dashboard

---

## 📋 **Option 2: Manual Setup (3 Terminal Windows)**

If you prefer manual control, here's the **correct order**:

### **Step 1: Start Backend Server (Terminal Window 1)**

1. Open a **NEW** Command Prompt or PowerShell window
2. Navigate to the project folder:
   ```cmd
   cd "C:\Users\Aayush Sharma\OneDrive\Desktop\hitl-ai-fair-lending-validation\backend"
   ```
3. Activate virtual environment:
   ```cmd
   venv\Scripts\activate
   ```
4. Start the backend:
   ```cmd
   python -m uvicorn app.main:app --reload --port 8000 --host 0.0.0.0
   ```
5. Wait until you see: `Uvicorn running on http://0.0.0.0:8000`
6. **KEEP THIS WINDOW OPEN!**

---

### **Step 2: Train ML Model (Terminal Window 2)**

**⚠️ IMPORTANT:** Do this AFTER backend starts, or do it first (recommended).

1. Open a **NEW** Command Prompt or PowerShell window
2. Navigate to backend:
   ```cmd
   cd "C:\Users\Aayush Sharma\OneDrive\Desktop\hitl-ai-fair-lending-validation\backend"
   venv\Scripts\activate
   ```
3. Run the training script:
   ```cmd
   python scripts\train_ml_model.py
   ```
4. Wait 1-2 minutes for completion
5. This will:
   - ✅ Import student profiles from datasets
   - ✅ Train the ML model
   - ✅ Score all profiles (fair + biased)
   - ✅ Calculate bias metrics
   - ✅ Dashboard will show metrics after this!

**Note:** You only need to do this ONCE (model is saved to disk)

---

### **Step 3: Start Frontend Server (Terminal Window 3)**

1. Open a **NEW** Command Prompt or PowerShell window
2. Navigate to the project folder:
   ```cmd
   cd "C:\Users\Aayush Sharma\OneDrive\Desktop\hitl-ai-fair-lending-validation\frontend"
   ```
3. Start the frontend:
   ```cmd
   npm run dev
   ```
4. Wait until you see: `Ready - started server on 0.0.0.0:3000`
5. **KEEP THIS WINDOW OPEN!**

---

## ✅ **What You Were Missing:**

Your steps were missing **Step 1 (Backend Server)**! The correct order is:

1. ✅ **Backend Server** (Terminal 1) - MUST run first
2. ✅ **Train ML Model** (Terminal 2) - Do once, or after backend
3. ✅ **Frontend Server** (Terminal 3) - Last

---

## 🎯 **Recommended Approach:**

**Use the batch file:**
```
run-complete-setup.bat
```

It does everything in the correct order automatically! 🚀

---

## 📊 **After Setup:**

Open browser:
- **Dashboard:** http://localhost:3000/dashboard
- **API Docs:** http://localhost:8000/docs

**Keep all 3 terminal windows open while using the application!**
