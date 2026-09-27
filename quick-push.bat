@echo off
REM Quick Push Script for GitHub
REM Usage: Double-click this file or run: quick-push.bat

echo ========================================
echo Quick GitHub Push
echo ========================================
echo.

echo [1/4] Checking git status...
git status
echo.

echo [2/4] Pulling latest changes...
git pull
if errorlevel 1 (
    echo WARNING: Pull failed. Continue anyway? (Y/N)
    set /p continue="> "
    if /i not "%continue%"=="Y" exit /b 1
)
echo.

echo [3/4] Adding all changes...
git add .
echo.

set /p message="[4/4] Enter commit message: "
if "%message%"=="" (
    echo ERROR: Commit message cannot be empty
    pause
    exit /b 1
)

git commit -m "%message%"
if errorlevel 1 (
    echo ERROR: Commit failed
    pause
    exit /b 1
)
echo.

echo Pushing to GitHub...
git push
if errorlevel 1 (
    echo ERROR: Push failed
    pause
    exit /b 1
)

echo.
echo ========================================
echo SUCCESS! Changes pushed to GitHub
echo ========================================
pause

