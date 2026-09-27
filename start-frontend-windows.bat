@echo off
REM Start Frontend Server on Windows

echo Starting Fair Lending AI Validation Frontend...
echo.

cd frontend

REM Check if node_modules exists
if not exist node_modules (
    echo ERROR: Dependencies not installed!
    echo Please run setup-windows.bat first
    pause
    exit /b 1
)

REM Start development server
echo Starting frontend server on http://localhost:3000
echo Press Ctrl+C to stop
echo.
call npm run dev

pause

