# Windows Setup Guide - Fair Lending AI Validation

This guide will help you set up the project on Windows 10/11.

## Prerequisites

Before starting, make sure you have:

1. **Python 3.11 or higher**
   - Download from: https://www.python.org/downloads/
   - During installation, check "Add Python to PATH"
   - Verify: Open Command Prompt and run `python --version`

2. **Node.js 18 or higher**
   - Download from: https://nodejs.org/
   - Choose the LTS version
   - Verify: Open Command Prompt and run `node --version`

3. **Git** (optional, for cloning)
   - Download from: https://git-scm.com/download/win

## Quick Setup (Automated)

### Option 1: Using the Setup Script

1. **Open Command Prompt** (cmd.exe) or **PowerShell**

2. **Navigate to the project directory:**
   ```cmd
   cd path\to\fair-lending-validation
   ```

3. **Run the setup script:**
   ```cmd
   setup-windows.bat
   ```

4. **Follow the prompts** - the script will:
   - Check Python and Node.js installations
   - Create virtual environment
   - Install all dependencies
   - Create configuration files

5. **Edit the API key:**
   - Open `backend\.env` in a text editor
   - Replace `your-gemini-api-key-here` with your actual Gemini API key

6. **Start the servers:**
   - **Backend**: Double-click `start-backend-windows.bat` or run:
     ```cmd
     cd backend
     venv\Scripts\activate
     python -m uvicorn app.main:app --reload --port 8000
     ```
   
   - **Frontend**: Double-click `start-frontend-windows.bat` or run (in a new terminal):
     ```cmd
     cd frontend
     npm run dev
     ```

7. **Open your browser:**
   - Go to: http://localhost:3000

## Manual Setup (Step-by-Step)

If the automated script doesn't work, follow these steps:

### Step 1: Backend Setup

1. **Open Command Prompt** and navigate to the project:
   ```cmd
   cd path\to\fair-lending-validation\backend
   ```

2. **Create virtual environment:**
   ```cmd
   python -m venv venv
   ```

3. **Activate virtual environment:**
   ```cmd
   venv\Scripts\activate
   ```
   You should see `(venv)` in your prompt.

4. **Upgrade pip:**
   ```cmd
   python -m pip install --upgrade pip
   ```

5. **Install dependencies:**
   ```cmd
   pip install -r requirements.txt
   ```

6. **Create .env file:**
   Create a file named `.env` in the `backend` folder with:
   ```env
   GEMINI_API_KEY=your-actual-gemini-api-key
   GEMINI_MODEL=gemini-2.0-flash
   DEBUG=True
   ENVIRONMENT=development
   DATABASE_URL=sqlite:///./fairlending.db
   CORS_ORIGINS=["http://localhost:3000", "http://localhost:3001"]
   ```

7. **Create uploads directory:**
   ```cmd
   mkdir uploads
   ```

### Step 2: Frontend Setup

1. **Open a new Command Prompt** and navigate to:
   ```cmd
   cd path\to\fair-lending-validation\frontend
   ```

2. **Install dependencies:**
   ```cmd
   npm install
   ```

3. **Create .env.local file:**
   Create a file named `.env.local` in the `frontend` folder with:
   ```
   NEXT_PUBLIC_API_URL=http://localhost:8000
   ```

### Step 3: Start the Servers

1. **Start Backend** (in first terminal):
   ```cmd
   cd backend
   venv\Scripts\activate
   python -m uvicorn app.main:app --reload --port 8000
   ```
   You should see: `Uvicorn running on http://0.0.0.0:8000`

2. **Start Frontend** (in second terminal):
   ```cmd
   cd frontend
   npm run dev
   ```
   You should see: `Ready on http://localhost:3000`

3. **Open Browser:**
   - Navigate to: http://localhost:3000

## Common Issues and Solutions

### Issue 1: "python is not recognized"

**Solution:**
- Python is not in your PATH
- Reinstall Python and check "Add Python to PATH"
- Or add Python manually to PATH:
  1. Find Python installation (usually `C:\Users\YourName\AppData\Local\Programs\Python\Python3XX`)
  2. Add to System PATH in Environment Variables

### Issue 2: "node is not recognized"

**Solution:**
- Node.js is not in your PATH
- Reinstall Node.js
- Or restart Command Prompt after installing Node.js

### Issue 3: "pip install fails"

**Solution:**
- Try upgrading pip first: `python -m pip install --upgrade pip`
- Use `python -m pip` instead of just `pip`
- Check your internet connection
- Some packages may need Visual C++ Build Tools (download from Microsoft)

### Issue 4: "npm install fails"

**Solution:**
- Clear npm cache: `npm cache clean --force`
- Delete `node_modules` folder and `package-lock.json`
- Run `npm install` again
- Check your internet connection

### Issue 5: "Port 8000 or 3000 already in use"

**Solution:**
- Find and close the process using the port:
  ```cmd
  netstat -ano | findstr :8000
  taskkill /PID <PID_NUMBER> /F
  ```
- Or change the port in the startup commands

### Issue 6: "Module not found" errors

**Solution:**
- Make sure virtual environment is activated (you should see `(venv)`)
- Reinstall dependencies: `pip install -r requirements.txt`
- Check you're in the correct directory

### Issue 7: "Cannot connect to backend"

**Solution:**
- Make sure backend is running (check terminal)
- Verify `.env.local` has correct API URL: `NEXT_PUBLIC_API_URL=http://localhost:8000`
- Check Windows Firewall isn't blocking the connection
- Try accessing http://localhost:8000/health directly in browser

## File Paths on Windows

The project uses Python's `pathlib.Path` which handles Windows paths automatically. However, if you encounter path issues:

- Use forward slashes `/` or double backslashes `\\` in paths
- Paths are relative to the project root
- Database file: `backend\fairlending.db`
- Uploads: `backend\uploads\`

## Using PowerShell Instead of CMD

All commands work the same in PowerShell. However:

- To activate virtual environment in PowerShell:
  ```powershell
  .\venv\Scripts\Activate.ps1
  ```
- If you get an execution policy error:
  ```powershell
  Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
  ```

## Development Workflow

1. **Always activate virtual environment** before working on backend:
   ```cmd
   cd backend
   venv\Scripts\activate
   ```

2. **Keep two terminals open:**
   - Terminal 1: Backend server (port 8000)
   - Terminal 2: Frontend server (port 3000)

3. **Hot Reload:**
   - Both servers support hot reload
   - Changes to code will automatically restart the server

4. **Stopping Servers:**
   - Press `Ctrl+C` in each terminal
   - Or close the terminal window

## Getting Your Gemini API Key

1. Go to: https://makersuite.google.com/app/apikey
2. Sign in with your Google account
3. Click "Create API Key"
4. Copy the key
5. Paste it in `backend\.env` file:
   ```
   GEMINI_API_KEY=your-copied-key-here
   ```

## Testing the Setup

1. **Backend Health Check:**
   - Open browser: http://localhost:8000/health
   - Should return: `{"status":"healthy"}`

2. **API Documentation:**
   - Open browser: http://localhost:8000/docs
   - Should show Swagger UI

3. **Frontend:**
   - Open browser: http://localhost:3000
   - Should show the dashboard

## Next Steps

Once everything is running:

1. Upload a ZIP file with student loan data through the dashboard
2. The system will process and import the data
3. View metrics and bias analysis on the dashboard
4. Provide feedback and run mitigation cycles

## Getting Help

If you encounter issues:

1. Check the error messages carefully
2. Verify all prerequisites are installed
3. Make sure virtual environment is activated
4. Check that both servers are running
5. Review the main README.md for more details

---

**Happy Coding on Windows! 🪟🚀**

