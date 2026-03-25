@echo off
setlocal enabledelayedexpansion

echo ========================================
echo   Test Bench Dashboard - Backend
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

REM Create virtual environment
if not exist "venv" (
    echo [INFO] Creating virtual environment...
    python -m venv venv
    if %errorlevel% neq 0 (
        echo [ERROR] Failed to create venv
        pause
        exit /b 1
    )
)

REM Create data directory
if not exist "data" mkdir data

REM Install dependencies
if not exist "venv\Lib\site-packages\fastapi" (
    echo [INFO] Installing dependencies...
    venv\Scripts\pip.exe install -r requirements.txt
)

echo.
echo [INFO] Starting backend server...
echo        http://localhost:8000
echo        http://localhost:8000/docs
echo.

venv\Scripts\python.exe -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
