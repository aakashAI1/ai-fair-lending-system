@echo off
REM Windows Setup Script for Fair Lending AI Validation
REM This script sets up the project on Windows

echo ========================================
echo Fair Lending AI Validation - Windows Setup
echo ========================================
echo.

REM Check Python
echo [1/7] Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.11+ from https://www.python.org/downloads/
    pause
    exit /b 1
)
python --version
echo.

REM Check Node.js
echo [2/7] Checking Node.js installation...
node --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Node.js is not installed or not in PATH
    echo Please install Node.js 18+ from https://nodejs.org/
    pause
    exit /b 1
)
node --version
echo.

REM Setup Backend
echo [3/7] Setting up backend...
cd backend
if not exist venv (
    echo Creating Python virtual environment...
    python -m venv venv
)
echo Activating virtual environment...
call venv\Scripts\activate.bat
echo Installing Python dependencies...
pip install --upgrade pip
pip install -r requirements.txt
if errorlevel 1 (
    echo ERROR: Failed to install Python dependencies
    pause
    exit /b 1
)
echo.

REM Create .env file if it doesn't exist
if not exist .env (
    echo Creating .env file...
    (
        echo GEMINI_API_KEY=your-gemini-api-key-here
        echo GEMINI_MODEL=gemini-2.0-flash
        echo DEBUG=True
        echo ENVIRONMENT=development
        echo DATABASE_URL=sqlite:///./fairlending.db
        echo CORS_ORIGINS=["http://localhost:3000", "http://localhost:3001"]
    ) > .env
    echo .env file created. Please edit it and add your API keys.
)
echo.

REM Setup Frontend
echo [4/7] Setting up frontend...
cd ..\frontend
if not exist node_modules (
    echo Installing Node.js dependencies...
    call npm install
    if errorlevel 1 (
        echo ERROR: Failed to install Node.js dependencies
        pause
        exit /b 1
    )
)
echo.

REM Create .env.local if it doesn't exist
if not exist .env.local (
    echo Creating .env.local file...
    echo NEXT_PUBLIC_API_URL=http://localhost:8000 > .env.local
)
echo.

cd ..

echo [5/7] Creating uploads directory...
if not exist backend\uploads mkdir backend\uploads
echo.

echo [6/7] Populating database with sample data...
cd backend
call venv\Scripts\activate.bat
python scripts\populate_mock_data.py
if errorlevel 1 (
    echo WARNING: Failed to populate sample data. You can run it manually later:
    echo   cd backend
    echo   venv\Scripts\activate
    echo   python scripts\populate_mock_data.py
) else (
    echo [OK] Sample data populated successfully!
)
cd ..
echo.

echo [7/7] Setup complete!
echo.
echo ========================================
echo Next Steps:
echo ========================================
echo.
echo 1. Edit backend\.env and add your Gemini API key:
echo    GEMINI_API_KEY=your-actual-api-key
echo    (Optional - only needed for GenAI profile generation)
echo.
echo 2. Start the backend server:
echo    Double-click start-backend-windows.bat
echo    OR: cd backend && venv\Scripts\activate && python -m uvicorn app.main:app --reload --port 8000
echo.
echo 3. In a new terminal, start the frontend:
echo    Double-click start-frontend-windows.bat
echo    OR: cd frontend && npm run dev
echo.
echo 4. Open http://localhost:3000/dashboard in your browser
echo    You should see sample metrics and data!
echo.
echo ========================================
pause

