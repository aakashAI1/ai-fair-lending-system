@echo off
REM Quick Showcase Script for AI Fair Lending Validation System (Windows)
REM This script helps you quickly set up and showcase the project

echo.
echo ============================================================
echo    AI Fair Lending Validation System - Quick Showcase Setup
echo ============================================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python not found. Please install Python 3.11+
    pause
    exit /b 1
)

REM Check if Node is installed
node --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Node.js not found. Please install Node.js
    pause
    exit /b 1
)

echo [OK] Prerequisites check passed
echo.

:menu
echo Select an option:
echo 1) Start Backend Server
echo 2) Start Frontend Server
echo 3) Show Quick Showcase Steps
echo 4) Exit
echo.
set /p choice="Enter choice [1-4]: "

if "%choice%"=="1" goto start_backend
if "%choice%"=="2" goto start_frontend
if "%choice%"=="3" goto show_steps
if "%choice%"=="4" goto end
goto menu

:start_backend
echo.
echo [INFO] Starting Backend Server...
cd backend
if not exist venv (
    echo Creating virtual environment...
    python -m venv venv
)
call venv\Scripts\activate.bat
pip install -r requirements.txt -q
echo [OK] Backend dependencies installed
echo [INFO] Starting backend on http://localhost:8000
echo [TIP] Press Ctrl+C to stop
echo.
python -m uvicorn app.main:app --reload --port 8000
goto end

:start_frontend
echo.
echo [INFO] Starting Frontend Server...
cd frontend
if not exist node_modules (
    echo Installing frontend dependencies...
    call npm install
)
echo [OK] Frontend dependencies installed
echo [INFO] Starting frontend on http://localhost:3000
echo [TIP] Press Ctrl+C to stop
echo.
call npm run dev
goto end

:show_steps
echo.
echo ============================================================
echo    Quick Showcase Steps
echo ============================================================
echo.
echo 1. Login (http://localhost:3000)
echo    - Admin: EMP001 / admin123
echo    - Analyst: EMP002 / analyst123
echo.
echo 2. Generate Profiles (200-300 profiles)
echo    - Go to Profiles -^> Generate
echo    - Select dimension (Rural vs Urban)
echo.
echo 3. Run Bias Analysis
echo    - Go to Bias Analysis
echo    - Select dimension -^> Run Analysis
echo.
echo 4. Provide Feedback
echo    - Go to Feedback
echo    - Submit expert feedback on detected bias
echo.
echo 5. Run Mitigation [KEY DEMO]
echo    - Go to Mitigation
echo    - Run 5-7 iterations
echo    - Show before/after improvements
echo.
echo Full guide: See SHOWCASE_GUIDE.md
echo.
pause
goto menu

:end
echo.
echo Goodbye!
pause
