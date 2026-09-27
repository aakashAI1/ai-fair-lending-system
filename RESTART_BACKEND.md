# Restart Backend Server

The backend server needs to be restarted to pick up the new training data.

## Steps:

1. **Stop the backend server:**
   - Find the terminal window where the backend is running
   - Press `Ctrl+C` to stop it
   - Or close that terminal window

2. **Start it again:**
   ```cmd
   cd backend
   venv\Scripts\activate
   python -m uvicorn app.main:app --reload --port 8000 --host 0.0.0.0
   ```

3. **Verify it's working:**
   - Wait for: `Uvicorn running on http://0.0.0.0:8000`
   - Open: http://localhost:8000/health (should show `{"status":"healthy"}`)

4. **Refresh the dashboard:**
   - Go to: http://localhost:3000/dashboard
   - Press `F5` or `Ctrl+F5` (hard refresh)

You should now see the correct metrics:
- Approval Parity: ~1.18
- Interest Gap: ~1.33%
- Collateral Gap: ~28.03%
- Fairness Score: ~51.3

