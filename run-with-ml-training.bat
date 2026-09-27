@echo off
REM Script to train ML model and run the project

echo ============================================================
echo Fair Lending AI Validation - ML Model Training and Setup
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
echo Training ML model on real datasets...
echo This will:
echo   1. Import both datasets
echo   2. Train ML model
echo   3. Score all profiles
echo   4. Calculate bias metrics
echo.
echo This may take a few minutes...
echo.

python scripts\train_ml_model.py

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ============================================================
    echo ML Model Training Complete!
    echo ============================================================
    echo.
    echo Next steps:
    echo   1. Start backend: start-backend-windows.bat (in a new window)
    echo   2. Start frontend: start-frontend-windows.bat (in another new window)
    echo   3. Open http://localhost:3000/dashboard
    echo.
    echo Your dashboard will show metrics from the trained ML model!
    echo.
) else (
    echo.
    echo Error occurred during training. Please check the error messages above.
)

pause

