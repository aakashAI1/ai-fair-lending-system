# How to Run the Project - Quick Guide 🚀

## ⚠️ IMPORTANT: You need 2 separate terminal windows!

### Step 1: Start Backend Server (Terminal Window 1)

1. Open **Command Prompt** or **PowerShell**
2. Navigate to the project folder:
   ```cmd
   cd "C:\Users\Aayush Sharma\OneDrive\Desktop\hitl-ai-fair-lending-validation\backend"
   ```
3. Activate virtual environment:
   ```cmd
   venv\Scripts\activate
   ```
   (You should see `(venv)` at the start of your prompt)
4. Start the backend:
   ```cmd
   python -m uvicorn app.main:app --reload --port 8000 --host 0.0.0.0
   ```
5. Wait until you see: `Uvicorn running on http://0.0.0.0:8000`
6. **KEEP THIS WINDOW OPEN!**

---

### Step 2: Start Frontend Server (Terminal Window 2)

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

### Step 3: Import Data & Train Model (Terminal Window 3)

**⚠️ IMPORTANT:** The dashboard will be empty until you import data!

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

---

### Step 4: Open Dashboard

1. Open your web browser (Chrome, Edge, Firefox)
2. Go to: **http://localhost:3000/dashboard**
3. **Refresh the page** (Ctrl+F5) if needed
4. You should now see:
   - ✅ Approval metrics (KPIs)
   - ✅ Bias heatmap with data
   - ✅ Top findings list

---

## 🐛 Troubleshooting

### Backend won't start?
- Make sure you're in the `backend` folder
- Make sure virtual environment is activated (you see `(venv)`)
- Check if port 8000 is free: `netstat -ano | findstr :8000`
- If port is busy, stop other processes using it

### Frontend won't start?
- Make sure you're in the `frontend` folder
- Check if `node_modules` exists (if not, run `npm install`)
- Check if port 3000 is free: `netstat -ano | findstr :3000`

### Can't see data on dashboard?
- **Did you run Step 3?** You must run `python scripts\train_ml_model.py` first!
- Make sure backend is running (check http://localhost:8000/health)
- Try refreshing the page (Ctrl+F5)
- Alternative: Use the "Upload Student Data" section on the dashboard (see below)

---

## ✅ Quick Verification

- Backend health: http://localhost:8000/health (should show `{"status":"healthy"}`)
- API docs: http://localhost:8000/docs
- Dashboard: http://localhost:3000/dashboard

---

## 📤 Alternative: Upload Your Own Data

Instead of using the training script, you can upload your own CSV files:

1. Go to: **http://localhost:3000/dashboard**
2. Find the **"Upload Student Data"** section at the top
3. Upload a CSV file with student profiles
4. The system will automatically:
   - Parse the CSV file
   - Map columns to student profile fields
   - Import profiles to the database
   - Create a new test run

**Note:** After uploading, you still need to:
- Score the profiles (use API: `POST /api/v1/scoring/fair` and `/scoring/biased`)
- Calculate metrics (use API: `POST /api/v1/metrics/calculate`)

**Why use upload instead of training script?**
- You have your own CSV files with student data
- You want to test with custom datasets
- You don't have the default datasets in `backend/data/` folder


