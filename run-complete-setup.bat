@echo off
REM ============================================================
REM Complete Project Setup - One-Click Start
REM Runs: ML Training, Backend Server, Frontend Server
REM ============================================================

echo.
echo ============================================================
echo   Fair Lending AI Validation - Complete Setup
echo ============================================================
echo.

REM Check if we're in the right directory
if not exist "backend" (
    echo ERROR: Please run this script from the project root directory!
    pause
    exit /b 1
)

REM ============================================================
REM Step 1: Train ML Model (if not already trained)
REM ============================================================
echo [Step 1/3] Checking ML Model Training...
echo.

cd backend

REM Activate virtual environment
if exist "venv\Scripts\activate.bat" (
    echo Activating virtual environment...
    call venv\Scripts\activate.bat
) else (
    echo ERROR: Virtual environment not found!
    echo Please run setup-windows.bat first.
    pause
    exit /b 1
)

REM Check if model already exists
if exist "models\scoring_model.pkl" (
    echo.
    echo [INFO] ML Model already exists at: models\scoring_model.pkl
    echo [INFO] Skipping training. To retrain, delete the model file first.
    echo.
    set SKIP_TRAINING=1
) else (
    echo.
    echo [INFO] ML Model not found. Starting training...
    echo.
    echo This will:
    echo   1. Import datasets
    echo   2. Train ML model
    echo   3. Create initial metrics
    echo.
    echo Please wait, this may take 1-2 minutes...
    echo.
    python scripts\train_ml_model.py
    if %ERRORLEVEL% NEQ 0 (
        echo.
        echo ERROR: ML Model training failed!
        echo Continuing anyway (you can train manually later)...
        echo.
    ) else (
        echo.
        echo [SUCCESS] ML Model training completed!
        echo.
    )
)

REM ============================================================
REM Step 2: Start Backend Server (New Window)
REM ============================================================
echo.
echo [Step 2/3] Starting Backend Server...
echo.
echo Opening backend server in a new window...
echo Backend will run on: http://localhost:8000
echo.

cd ..
echo Opening backend server window (will be titled "Fair Lending - Backend Server")...
start "Fair Lending - Backend Server" cmd /k "cd /d %~dp0backend && venv\Scripts\activate.bat && echo ============================================================ && echo   BACKEND SERVER && echo ============================================================ && echo. && echo Starting on http://localhost:8000 && echo. && echo If you don't see this window, check your taskbar! && echo. && python -m uvicorn app.main:app --reload --port 8000 --host 0.0.0.0"

REM Wait a bit for backend to start
timeout /t 3 /nobreak >nul

REM ============================================================
REM Step 3: Start Frontend Server (New Window)
REM ============================================================
echo.
echo [Step 3/3] Starting Frontend Server...
echo.
echo Opening frontend server in a new window...
echo Frontend will run on: http://localhost:3000
echo.

echo Opening frontend server window (will be titled "Fair Lending - Frontend Server")...
start "Fair Lending - Frontend Server" cmd /k "cd /d %~dp0frontend && echo ============================================================ && echo   FRONTEND SERVER && echo ============================================================ && echo. && echo Starting on http://localhost:3000 && echo. && echo If you don't see this window, check your taskbar! && echo. && npm run dev"

REM Wait a bit for frontend to start
timeout /t 3 /nobreak >nul

REM ============================================================
REM Summary
REM ============================================================
echo.
echo ============================================================
echo   Setup Complete!
echo ============================================================
echo.
echo Two new windows should have opened:
echo   1. "Fair Lending - Backend Server" - http://localhost:8000
echo   2. "Fair Lending - Frontend Server" - http://localhost:3000
echo.
echo If you don't see the windows:
echo   - Check your taskbar (they might be minimized)
echo   - Press Alt+Tab to switch between windows
echo   - Look for windows titled "Fair Lending - Backend Server" and "Fair Lending - Frontend Server"
echo.
echo The application will be available at:
echo   Dashboard: http://localhost:3000/dashboard
echo   API Docs:  http://localhost:8000/docs
echo.
echo NOTE: Keep the backend and frontend windows open!
echo       Close this window if you want.
echo.
echo ============================================================
echo.

REM Keep window open
pause
