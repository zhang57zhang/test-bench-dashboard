@echo off
echo ========================================
echo   Development Mode Startup
echo ========================================
echo.

cd /d %~dp0

REM Start Backend
echo [1/2] Starting backend (dev mode)...
start "Backend Dev" cmd /k "cd backend && python -m venv venv && venv\Scripts\activate && pip install -r requirements.txt && python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000"

timeout /t 8 /nobreak >nul

REM Start Frontend
echo [2/2] Starting frontend (dev mode)...
cd frontend

start "Frontend Dev" cmd /k "npm run dev"

echo.
echo ========================================
echo   Development servers started!
echo ========================================
echo.
echo Frontend: http://localhost:3000
echo Backend:  http://localhost:8000
echo API Docs: http://localhost:8000/docs
echo.
pause
