@echo off
echo ========================================
echo Starting Frontend Server
echo ========================================
echo.

cd /d "%~dp0frontend"

if not exist "node_modules" (
    echo ERROR: Dependencies not installed!
    echo Please run setup-windows.bat first
    pause
    exit /b 1
)

echo Starting frontend on http://localhost:3000
echo Press Ctrl+C to stop
echo.
echo DO NOT CLOSE THIS WINDOW!
echo.

call npm run dev

pause


