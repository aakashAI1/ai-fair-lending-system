@echo off
echo ========================================
echo Starting Backend Server
echo ========================================
echo.

cd /d "%~dp0backend"

if not exist "venv\Scripts\activate.bat" (
    echo ERROR: Virtual environment not found!
    echo Please run setup-windows.bat first
    pause
    exit /b 1
)

call venv\Scripts\activate.bat

echo Starting backend on http://localhost:8000
echo Press Ctrl+C to stop
echo.
echo DO NOT CLOSE THIS WINDOW!
echo.

python -m uvicorn app.main:app --reload --port 8000 --host 0.0.0.0

pause

