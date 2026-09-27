# Quick Run Guide 🚀

## Running the Project (3 Steps)

### Step 1: Start Backend
**Windows:**
- Double-click `start-backend-windows.bat`
- OR: Open terminal, run:
  ```cmd
  cd backend
  venv\Scripts\activate
  python -m uvicorn app.main:app --reload --port 8000
  ```

**Mac/Linux:**
- Run: `./start-backend.sh`
- OR: Open terminal, run:
  ```bash
  cd backend
  source venv/bin/activate
  python3 -m uvicorn app.main:app --reload --port 8000
  ```

**Verify:** Open http://localhost:8000/health (should show `{"status": "healthy"}`)

### Step 2: Start Frontend
**Windows:**
- Double-click `start-frontend-windows.bat` (in a NEW window)
- OR: Open new terminal, run:
  ```cmd
  cd frontend
  npm run dev
  ```

**Mac/Linux:**
- Run in new terminal: `./start-frontend.sh`
- OR: Open new terminal, run:
  ```bash
  cd frontend
  npm run dev
  ```

**Verify:** Open http://localhost:3000 (should show the app)

### Step 3: Open Dashboard
- Open browser: **http://localhost:3000/dashboard**
- You should see all metrics! ✅

---

## Quick Commands Reference

| Task | Windows | Mac/Linux |
|------|---------|-----------|
| **Start Backend** | `start-backend-windows.bat` | `./start-backend.sh` |
| **Start Frontend** | `start-frontend-windows.bat` | `./start-frontend.sh` |
| **Stop Backend** | Press `Ctrl+C` in backend terminal | Press `Ctrl+C` in backend terminal |
| **Stop Frontend** | Press `Ctrl+C` in frontend terminal | Press `Ctrl+C` in frontend terminal |

---

## First Time Setup (Only Once)

If you haven't set up yet:

**Windows:**
```cmd
setup-windows.bat
```

**Mac/Linux:**
```bash
chmod +x setup.sh start-backend.sh start-frontend.sh
./setup.sh
```

This will:
- Install all dependencies
- Create virtual environment
- **Automatically populate sample data**

---

## Troubleshooting

### "Backend not starting"
- Check if port 8000 is free: `netstat -ano | findstr :8000` (Windows)
- Make sure virtual environment is activated
- Check `backend/.env` exists

### "Frontend not starting"
- Check if port 3000 is free
- Make sure `node_modules` is installed: `cd frontend && npm install`
- Check `frontend/.env.local` exists

### "No data on dashboard"
- Run: `cd backend && python scripts/populate_mock_data.py` (Windows)
- Run: `cd backend && python3 scripts/populate_mock_data.py` (Mac/Linux)

---

## URLs

- **Frontend Dashboard**: http://localhost:3000/dashboard
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health

---

**That's it!** Just start backend, start frontend, and open the dashboard! 🎉

