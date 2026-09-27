# How to Run the Project - Complete Guide 🚀

## Prerequisites Check

Before running, make sure you have:
- ✅ Python 3.11+ installed
- ✅ Node.js 18+ installed  
- ✅ Virtual environment created (or we'll create it)
- ✅ Dependencies installed (or we'll install them)

---

## Quick Start (Windows) 🪟

### Option 1: Using Batch Files (Easiest)

**You need 2 separate terminal windows:**

1. **Terminal 1 - Start Backend:**
   - Double-click `start-backend-windows.bat` 
   - OR open Command Prompt and run:
     ```cmd
     start-backend-windows.bat
     ```
   - Wait until you see: `Uvicorn running on http://0.0.0.0:8000`
   - **Keep this window open!**

2. **Terminal 2 - Start Frontend:**
   - Double-click `start-frontend-windows.bat`
   - OR open Command Prompt and run:
     ```cmd
     start-frontend-windows.bat
     ```
   - Wait until you see: `Ready - started server on 0.0.0.0:3000`
   - **Keep this window open!**

3. **Open Browser:**
   - Go to: **http://localhost:3000/dashboard**
   - You should see the dashboard!

### Option 2: Manual Commands

**Terminal 1 - Backend:**
```cmd
cd backend
venv\Scripts\activate
python -m uvicorn app.main:app --reload --port 8000 --host 0.0.0.0
```

**Terminal 2 - Frontend (NEW WINDOW):**
```cmd
cd frontend
npm run dev
```

**Open Browser:** http://localhost:3000/dashboard

---

## First Time Setup (If Needed)

If you haven't set up yet, run this first:

### Windows:
```cmd
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
cd ..\frontend
npm install
```

### Create .env file (Backend):
```cmd
cd backend
python setup_env.py
```

This will automatically create the `.env` file with your Gemini API key configured.

Alternatively, manually create `backend\.env` with:
```
GEMINI_API_KEY=your_gemini_api_key_here
DATABASE_URL=sqlite:///./fairlending.db
DEBUG=True
CORS_ORIGINS=["http://localhost:3000", "http://localhost:3001"]
```

---

## Verification Steps ✅

### 1. Check Backend is Running
- Open: http://localhost:8000/health
- Should show: `{"status": "healthy"}`

### 2. Check API Documentation
- Open: http://localhost:8000/docs
- Should show Swagger UI with all endpoints

### 3. Check Frontend is Running
- Open: http://localhost:3000
- Should redirect to `/dashboard`

### 4. Check Dashboard Has Data
- If you've trained the ML model, you should see metrics
- If not, you'll see empty metrics/heatmap (this is normal - see next section)

⚠️ **IMPORTANT:** If dashboard shows empty metrics, you need to import data first (see "Training ML Model" section below)

---

## Training ML Model (Optional but Recommended)

To see actual bias metrics on the dashboard:

1. **Open a new terminal window**

2. **Navigate to backend:**
   ```cmd
   cd backend
   venv\Scripts\activate
   ```

3. **Run training script:**
   ```cmd
   python scripts/train_ml_model.py
   ```

4. **Wait for completion** (takes 1-2 minutes)

5. **Refresh dashboard** (http://localhost:3000/dashboard)
   - You should now see metrics!

---

## Troubleshooting 🔧

### Backend won't start?

**Error: "No module named 'xxx'"**
```cmd
cd backend
venv\Scripts\activate
pip install -r requirements.txt
```

**Error: "Address already in use" (Port 8000)**
- Check if port is in use: `netstat -ano | findstr :8000`
- Kill the process or change port: `--port 8001`

**Error: "venv not found"**
```cmd
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

### Frontend won't start?

**Error: "node_modules not found"**
```cmd
cd frontend
npm install
```

**Error: "Port 3000 already in use"**
- Kill the process or change port: `npm run dev -- -p 3001`

### Dashboard shows "No test data available"?

This is normal if you haven't:
1. Trained the ML model, OR
2. Generated/imported profiles, OR
3. Calculated metrics

**To fix:**
- Train the ML model (see above), OR
- Use the Data Upload component on dashboard to upload CSV files

### Can't connect to backend?

1. Check backend is running: http://localhost:8000/health
2. Check CORS settings in `backend/app/config.py`
3. Check frontend `.env.local` has: `NEXT_PUBLIC_API_URL=http://localhost:8000`

---

## Project Structure Quick Reference

```
hitl-ai-fair-lending-validation/
├── backend/                 # FastAPI backend
│   ├── app/                # Main application code
│   ├── scripts/            # Utility scripts (train_ml_model.py)
│   ├── venv/               # Virtual environment (created)
│   ├── .env                # Environment variables (create this)
│   └── requirements.txt    # Python dependencies
│
├── frontend/               # Next.js frontend
│   ├── app/                # Pages and components
│   ├── node_modules/       # Dependencies (created after npm install)
│   └── package.json        # Node dependencies
│
└── *.csv                   # Training datasets (if present)
```

---

## What to Expect

### When Backend Starts Successfully:
```
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [xxxxx]
INFO:     Started server process [xxxxx]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

### When Frontend Starts Successfully:
```
▲ Next.js 14.0.4
- Local:        http://localhost:3000
- Ready in 2.5s
```

### When Dashboard Loads:
- **With data**: KPI cards, heatmap, top findings
- **Without data**: Welcome message with setup instructions

---

## Key URLs

| Service | URL | Purpose |
|---------|-----|---------|
| **Frontend Dashboard** | http://localhost:3000/dashboard | Main dashboard |
| **Frontend Home** | http://localhost:3000 | Redirects to dashboard |
| **Backend API** | http://localhost:8000 | REST API |
| **API Docs** | http://localhost:8000/docs | Swagger UI |
| **Health Check** | http://localhost:8000/health | Backend status |

---

## Common Commands Reference

### Backend Commands:
```cmd
# Activate virtual environment
cd backend
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Start server
python -m uvicorn app.main:app --reload --port 8000

# Train ML model
python scripts/train_ml_model.py

# Check database
python scripts/check_data.py
```

### Frontend Commands:
```cmd
# Install dependencies
cd frontend
npm install

# Start dev server
npm run dev

# Build for production
npm run build

# Start production server
npm start
```

---

## Stopping the Servers

**To stop backend or frontend:**
- Press `Ctrl+C` in the terminal window where it's running
- Wait for the process to stop gracefully

**To kill stuck processes:**
- Windows: `taskkill /F /IM python.exe` (backend) or `taskkill /F /IM node.exe` (frontend)
- Or use Task Manager

---

## Next Steps After Running

1. ✅ Verify both servers are running
2. ✅ Open dashboard: http://localhost:3000/dashboard
3. ✅ (Optional) Train ML model to see real metrics
4. ✅ Explore the dashboard, bias analysis, feedback, and mitigation pages
5. ✅ Check API documentation: http://localhost:8000/docs

---

## Need Help?

- Check the console/terminal output for error messages
- Verify all prerequisites are installed
- Make sure ports 8000 and 3000 are free
- Check that `.env` file exists in `backend/` directory
- Review this guide's troubleshooting section

**Everything should work out of the box if dependencies are installed!** 🎉

