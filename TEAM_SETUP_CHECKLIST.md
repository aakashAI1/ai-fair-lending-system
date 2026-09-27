# Team Setup Checklist ✅

## What Your Teammates Need to Do

### Step 1: Clone the Repository
```bash
git clone https://github.com/aayusharmaaa/hitl-project-testing.git
cd hitl-project-testing
```

### Step 2: Run Setup Script

**Windows:**
```cmd
setup-windows.bat
```

**Mac/Linux:**
```bash
chmod +x setup.sh start-backend.sh start-frontend.sh
./setup.sh
```

### Step 3: Start the Application

**Windows:**
- Double-click `start-backend-windows.bat` (opens in new window)
- Double-click `start-frontend-windows.bat` (opens in new window)

**Mac/Linux:**
- Terminal 1: `./start-backend.sh`
- Terminal 2: `./start-frontend.sh`

### Step 4: Open Dashboard
- Open browser: http://localhost:3000/dashboard
- **You should see all metrics!** ✅

---

## What Happens Automatically

When teammates run the setup script, it will:

1. ✅ Check Python and Node.js installation
2. ✅ Create Python virtual environment
3. ✅ Install all backend dependencies
4. ✅ Install all frontend dependencies
5. ✅ Create `.env` file (if doesn't exist)
6. ✅ Create `.env.local` file (if doesn't exist)
7. ✅ Create uploads directory
8. ✅ **Automatically populate sample data** (100 profiles, metrics, etc.)

---

## What They'll See

After setup and starting servers:

### Dashboard (`http://localhost:3000/dashboard`)
- ✅ 4 KPI Cards (Approval Parity, Interest Gap, Collateral Gap, Fairness Score)
- ✅ Bias Heatmap visualization
- ✅ Top 3 Findings list

### Bias Analysis (`http://localhost:3000/bias-analysis`)
- ✅ Filterable table with 3 bias metrics
- ✅ Profile comparison view

### Feedback (`http://localhost:3000/feedback`)
- ✅ Feedback form with 2 existing feedback entries

### Mitigation (`http://localhost:3000/mitigation`)
- ✅ Mitigation form
- ✅ Comparison table with 2 iterations

---

## Troubleshooting

### "No data visible on dashboard"
**Solution:**
```bash
cd backend
# Windows:
venv\Scripts\activate
python scripts\populate_mock_data.py

# Mac/Linux:
source venv/bin/activate
python3 scripts/populate_mock_data.py
```

### "Backend not starting"
**Check:**
1. Virtual environment activated?
2. `.env` file exists in `backend/`?
3. Port 8000 available?

### "Frontend not starting"
**Check:**
1. `node_modules` installed? (run `npm install` in `frontend/`)
2. `.env.local` exists in `frontend/`?
3. Port 3000 available?

### "API connection error"
**Check:**
1. Backend running? (http://localhost:8000/health)
2. `frontend/.env.local` has: `NEXT_PUBLIC_API_URL=http://localhost:8000`

---

## Files They'll Get

When cloning, teammates will receive:
- ✅ All source code
- ✅ Setup scripts (Windows + Mac/Linux)
- ✅ Configuration files
- ✅ Documentation
- ✅ Sample data generation script

**They will NOT get:**
- ❌ Database file (`.db` files are gitignored - each person gets their own)
- ❌ `.env` files (gitignored - each person creates their own)
- ❌ `node_modules` (gitignored - installed during setup)
- ❌ `venv` (gitignored - created during setup)

---

## Verification

After setup, teammates can verify everything works:

1. **Check Backend:**
   ```bash
   curl http://localhost:8000/health
   # Should return: {"status": "healthy"}
   ```

2. **Check Dashboard API:**
   ```bash
   curl http://localhost:8000/api/v1/dashboard
   # Should return JSON with metrics
   ```

3. **Check Frontend:**
   - Open http://localhost:3000/dashboard
   - Should see KPI cards with numbers (not zeros)

---

## Quick Reference

| Task | Windows | Mac/Linux |
|------|---------|-----------|
| Setup | `setup-windows.bat` | `./setup.sh` |
| Start Backend | `start-backend-windows.bat` | `./start-backend.sh` |
| Start Frontend | `start-frontend-windows.bat` | `./start-frontend.sh` |
| Populate Data | `python scripts\populate_mock_data.py` | `python3 scripts/populate_mock_data.py` |

---

## Support

If teammates encounter issues:
1. Check `CROSS_PLATFORM_SETUP.md` for compatibility issues
2. Check `QUICK_DATA_SETUP.md` for data population issues
3. Check `FEATURE_TEST_REPORT.md` for feature status
4. Check main `README.md` for general setup

---

**✅ Everything is ready!** Your teammates just need to:
1. Clone the repo
2. Run setup script
3. Start servers
4. See the dashboard with all metrics!

