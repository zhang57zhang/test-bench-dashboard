@echo off
echo ========================================
echo   Start and Test DVP
echo ========================================
echo.

cd /d %~dp0

REM Step 1: Start backend
echo Step 1: Starting backend...
start "Backend" cmd /k "cd backend && start.bat"

echo Waiting 10 seconds for backend to start...
timeout /t 10 /nobreak >nul

REM Step 2: Test backend
echo.
echo Step 2: Testing backend health...
powershell -Command "$health = Invoke-RestMethod -Uri 'http://localhost:8000/health' -ErrorAction SilentlyContinue; if ($health.status -eq 'healthy') { Write-Host '[OK] Backend is healthy' } else { Write-Host '[ERROR] Backend not responding' }"

REM Step 3: Test DVP API
echo.
echo Step 3: Testing DVP API...
powershell -Command "$projects = Invoke-RestMethod -Uri 'http://localhost:8000/api/v1/dvp/projects' -ErrorAction SilentlyContinue; if ($projects) { Write-Host '[OK] DVP API working'; Write-Host 'Total projects:' $projects.Count } else { Write-Host '[ERROR] DVP API not responding' }"

echo.
echo ========================================
echo   Test Complete!
echo ========================================
echo.
echo Next steps:
echo   1. Open browser: http://localhost:3000
echo   2. Click dashboard selector
echo   3. Choose "DVP Progress Dashboard"
echo.
pause
