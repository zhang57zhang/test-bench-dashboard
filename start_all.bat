@echo off
echo ========================================
echo   Start All Services
echo ========================================
echo.

cd /d %~dp0

REM Start Backend
echo [1/2] Starting backend server...
start "Backend" cmd /k "cd backend && python -m venv venv && venv\Scripts\activate && pip install -r requirements.txt && python -m uvicorn app.main:app --host 0.0.0.0 --port 8000"

timeout /t 8 /nobreak >nul

REM Start Frontend
echo [2/2] Starting frontend server...
cd frontend

if not exist "out\index.html" (
    echo Building frontend...
    call npm run build
)

start "Frontend" cmd /k "serve -s out -l 3000"

echo.
echo ========================================
echo   All services started successfully!
echo ========================================
echo.
echo Frontend: http://localhost:3000
echo Backend:  http://localhost:8000
echo API Docs: http://localhost:8000/docs
echo.
pause
