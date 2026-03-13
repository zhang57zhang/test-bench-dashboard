@echo off
echo ========================================
echo   Simple Startup Script
echo ========================================
echo.

cd /d %~dp0

echo Step 1: Starting backend...
start "Backend Server" cmd /k "cd backend && start.bat"

timeout /t 10 /nobreak >nul

echo Step 2: Starting frontend...
cd frontend

if exist "out\index.html" (
    echo Frontend already built, starting server...
    start "Frontend Server" cmd /k "serve -s out -l 3000"
) else (
    echo Building frontend first...
    call npm run build
    start "Frontend Server" cmd /k "serve -s out -l 3000"
)

echo.
echo ========================================
echo   All services started!
echo ========================================
echo.
echo Open your browser and visit:
echo   http://localhost:3000
echo.
pause
