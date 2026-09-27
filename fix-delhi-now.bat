@echo off
REM Quick fix script to clear old profiles and regenerate with correct states
echo ============================================================
echo FIXING DELHI PROBLEM - CLEARING OLD DATA AND REGENERATING
echo ============================================================
echo.

cd backend

REM Activate venv
call venv\Scripts\activate.bat

echo [1/2] Clearing all old profiles...
python scripts\clear_all_profiles.py

echo.
echo [2/2] Regenerating profiles with correct state distribution...
python scripts\train_ml_model.py

echo.
echo ============================================================
echo DONE! Now refresh your frontend (Ctrl+Shift+R)
echo You should see diverse states now!
echo ============================================================
pause
