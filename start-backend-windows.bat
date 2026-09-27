@echo off
REM Start Backend Server on Windows

echo Starting Fair Lending AI Validation Backend...
echo.

cd backend

REM Check if virtual environment exists
if not exist venv (
    echo ERROR: Virtual environment not found!
    echo Please run setup-windows.bat first
    pause
    exit /b 1
)

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Check if .env exists
if not exist .env (
    echo WARNING: .env file not found!
    echo Please create .env file with your API keys.
    pause
)

REM Start server
echo Starting backend server on http://localhost:8000
echo Press Ctrl+C to stop
echo.
python -m uvicorn app.main:app --reload --port 8000 --host 0.0.0.0

pause

