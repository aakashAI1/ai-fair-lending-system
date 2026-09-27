@echo off
REM Setup script for Windows to generate showcase data
echo ============================================================
echo Fair Lending AI Validation - Showcase Data Setup
echo ============================================================
echo.

cd backend

REM Check if virtual environment exists
if exist "venv\Scripts\activate.bat" (
    echo Activating virtual environment...
    call venv\Scripts\activate.bat
) else (
    echo Virtual environment not found. Please run setup-windows.bat first.
    pause
    exit /b 1
)

echo.
echo Generating showcase data...
echo This may take a few minutes...
echo.

python scripts\setup_showcase_data.py

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ============================================================
    echo Setup complete! Your dashboard is ready for showcase.
    echo ============================================================
    echo.
    echo Next steps:
    echo   1. Make sure backend is running: start-backend-windows.bat
    echo   2. Make sure frontend is running: start-frontend-windows.bat
    echo   3. Open http://localhost:3000/dashboard
    echo.
) else (
    echo.
    echo Error occurred during setup. Please check the error messages above.
)

pause

