@echo off
echo ========================================
echo   DVP Dashboard Test Script
echo ========================================
echo.

cd /d %~dp0

REM Start Backend
echo [1/3] Starting backend server...
if exist "backend\start.bat" (
    start "Backend Server" cmd /k "cd /d %~dp0backend && start.bat"
    echo [OK] Backend starting...
) else (
    echo [ERROR] backend\start.bat not found
    pause
    exit /b 1
)

REM Wait for backend
echo Waiting for backend to initialize...
timeout /t 10 /nobreak >nul

REM Test backend health
echo [2/3] Testing backend API...
powershell -Command "try { $response = Invoke-WebRequest -Uri 'http://localhost:8000/health' -UseBasicParsing -TimeoutSec 5; if ($response.StatusCode -eq 200) { exit 0 } else { exit 1 } } catch { exit 1 }"

if %errorlevel% equ 0 (
    echo [OK] Backend API is responding
) else (
    echo [ERROR] Backend API not responding
    echo Please check if backend started correctly
    pause
    exit /b 1
)

REM Test DVP API
echo [3/3] Testing DVP API...
powershell -Command "try { $response = Invoke-WebRequest -Uri 'http://localhost:8000/api/v1/dvp/projects' -UseBasicParsing -TimeoutSec 5; if ($response.StatusCode -eq 200) { exit 0 } else { exit 1 } } catch { exit 1 }"

if %errorlevel% equ 0 (
    echo [OK] DVP API is responding
) else (
    echo [ERROR] DVP API not responding
    echo Please check DVP router configuration
    pause
    exit /b 1
)

echo.
echo ========================================
echo   All Tests Passed!
echo ========================================
echo.
echo Backend Server: http://localhost:8000
echo API Docs:       http://localhost:8000/docs
echo DVP API:        http://localhost:8000/api/v1/dvp/projects
echo.
echo You can now:
echo   1. Open http://localhost:3000 in browser
echo   2. Switch to DVP Dashboard
echo.
pause
