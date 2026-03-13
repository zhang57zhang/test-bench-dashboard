@echo off
setlocal enabledelayedexpansion

echo.
echo ========================================
echo   Unified Dashboard Platform
echo   All Services Startup
echo ========================================
echo.

REM Change to script directory
cd /d "%~dp0"

REM ========================================
REM Check prerequisites
REM ========================================

echo Checking prerequisites...

REM Check Python
where python >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python not found
    echo Please install Python 3.10 or higher
    pause
    exit /b 1
)

REM Check Node.js
where node >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Node.js not found
    echo Please install Node.js 18 or higher
    pause
    exit /b 1
)

echo [OK] Prerequisites check passed
echo.

REM ========================================
REM Start Backend
REM ========================================

echo [1/2] Starting backend server...

if exist "backend\start.bat" (
    start "Backend Server" cmd /k "cd /d "%~dp0backend" && start.bat"
    echo [OK] Backend starting...
) else (
    echo [WARNING] backend\start.bat not found
    echo Creating backend startup command...
    start "Backend Server" cmd /k "cd /d "%~dp0backend" && python -m venv venv && venv\Scripts\activate && pip install -r requirements.txt && python -m uvicorn app.main:app --host 0.0.0.0 --port 8000"
)

REM Wait for backend to start
echo Waiting for backend to initialize...
timeout /t 8 /nobreak >nul

REM ========================================
REM Start Frontend
REM ========================================

echo [2/2] Starting frontend server...

cd /d "%~dp0frontend"

REM Check if build exists
if not exist "out\index.html" (
    echo Frontend not built, building now...
    call npm run build
    if %errorlevel% neq 0 (
        echo [ERROR] Frontend build failed
        pause
        exit /b 1
    )
)

REM Check if serve is installed
where serve >nul 2>&1
if %errorlevel% neq 0 (
    echo Installing serve globally...
    call npm install -g serve
)

REM Start frontend server
start "Frontend Server" cmd /k "cd /d "%~dp0frontend" && serve -s out -l 3000"
echo [OK] Frontend starting...

REM Wait for frontend to start
timeout /t 3 /nobreak >nul

REM ========================================
REM Display access information
REM ========================================

echo.
echo ========================================
echo   All Services Started Successfully!
echo ========================================
echo.
echo Access URLs:
echo   Frontend:  http://localhost:3000
echo   Backend:   http://localhost:8000
echo   API Docs:  http://localhost:8000/docs
echo.
echo Available Dashboards:
echo   1. Test Bench Dashboard
echo   2. DVP Progress Dashboard
echo   3. Automation Test Dashboard
echo   4. AI Assistant Dashboard
echo.
echo ========================================
echo.

REM Open browser
echo Opening browser...
start http://localhost:3000

echo.
echo Press any key to exit this window...
echo (Services will continue running in background)
pause >nul
