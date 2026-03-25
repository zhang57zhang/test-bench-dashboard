@echo off
setlocal enabledelayedexpansion

echo ========================================
echo   Test Bench Dashboard - Quick Start
echo ========================================
echo.

cd /d "%~dp0"

REM Check Python
where python >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python not found. Please install Python 3.10+
    echo         Download: https://www.python.org/downloads/
    pause
    exit /b 1
)

REM Check Node.js
where node >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Node.js not found. Please install Node.js 18+
    echo         Download: https://nodejs.org/
    pause
    exit /b 1
)

echo [1/2] Starting Backend Server...
cd backend

REM Create virtual environment
if not exist "venv" (
    echo [INFO] Creating Python virtual environment...
    python -m venv venv
    if %errorlevel% neq 0 (
        echo [ERROR] Failed to create virtual environment
        pause
        exit /b 1
    )
)

REM Create data directory
if not exist "data" mkdir data

REM Check and install dependencies
if not exist "venv\Lib\site-packages\fastapi" (
    echo [INFO] Installing backend dependencies...
    venv\Scripts\pip.exe install -r requirements.txt
    if %errorlevel% neq 0 (
        echo [ERROR] Failed to install dependencies
        pause
        exit /b 1
    )
)

REM Start backend server
echo [INFO] Starting backend on port 8000...
start "Backend - Port 8000" cmd /c "cd /d %~dp0backend && venv\Scripts\python.exe -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload"

echo.
echo   Backend:  http://localhost:8000
echo   API Docs: http://localhost:8000/docs
echo.

REM Wait for backend to start
echo [INFO] Waiting for backend to start...
ping -n 6 127.0.0.1 >nul 2>&1

echo [2/2] Starting Frontend Server...
cd ..\frontend

REM Install frontend dependencies
if not exist "node_modules" (
    echo [INFO] Installing frontend dependencies...
    call npm install
    if %errorlevel% neq 0 (
        echo [ERROR] Failed to install npm dependencies
        pause
        exit /b 1
    )
)

REM Start frontend server
echo [INFO] Starting frontend on port 3000...
start "Frontend - Port 3000" cmd /c "cd /d %~dp0frontend && npm run dev"

echo.
echo   Frontend: http://localhost:3000
echo.

echo ========================================
echo   Services Started Successfully!
echo ========================================
echo.
echo   Frontend: http://localhost:3000
echo   Backend:  http://localhost:8000
echo   API Docs: http://localhost:8000/docs
echo.
echo   Press any key to open browser...
pause >nul

start "" http://localhost:3000

echo.
echo [INFO] Browser opened. You can close this window.
echo        Close the Backend/Frontend windows to stop servers.
