@echo off
setlocal enabledelayedexpansion

echo ========================================
echo   Test Bench Dashboard - Frontend
echo ========================================
echo.

cd /d "%~dp0"

REM Check Node.js
where node >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Node.js not found
    echo Please install Node.js 18+ from https://nodejs.org/
    pause
    exit /b 1
)

REM Install dependencies
if not exist "node_modules" (
    echo [INFO] Installing dependencies...
    call npm install
)

echo.
echo [INFO] Starting frontend server...
echo        http://localhost:3000
echo.

call npm run dev
