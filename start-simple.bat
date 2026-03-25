@echo off
setlocal enabledelayedexpansion

echo ========================================
echo   Test Bench Dashboard
echo   Quick Start Script
echo ========================================
echo.

cd /d "%~dp0"

REM Check Python
where python >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python not found
    echo Please install Python 3.10+ from https://www.python.org/
    pause
    exit /b 1
)

REM Check Node.js
where node >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Node.js not found
    echo Please install Node.js 18+ from https://nodejs.org/
    pause
    exit /b 1
)

REM === Backend Setup ===
echo [1/2] Setting up backend...
cd backend

if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
)

if not exist "data" mkdir data

if not exist "venv\Lib\site-packages\fastapi" (
    echo Installing dependencies...
    venv\Scripts\pip.exe install -r requirements.txt -q
)

echo Starting backend server...
start "Backend-8000" cmd /c "cd /d %~dp0backend && venv\Scripts\python.exe -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload"

echo   Backend:  http://localhost:8000
echo   API Docs: http://localhost:8000/docs

ping -n 5 127.0.0.1 >nul 2>&1

REM === Frontend Setup ===
echo.
echo [2/2] Setting up frontend...
cd ..\frontend

if not exist "node_modules" (
    echo Installing dependencies...
    call npm install --silent
)

echo Starting frontend server...
start "Frontend-3000" cmd /c "cd /d %~dp0frontend && npm run dev"

echo   Frontend: http://localhost:3000

echo.
echo ========================================
echo   Done! Servers are running.
echo ========================================
echo.
echo   Close this window to exit.
echo   Or press any key to open browser...
pause >nul

start "" http://localhost:3000
