@echo off
echo ========================================
echo   Quick DVP Test
echo ========================================
echo.

echo Testing backend API...
powershell -Command "$result = Invoke-RestMethod -Uri 'http://localhost:8000/api/v1/dvp/projects' -Method Get -ErrorAction SilentlyContinue; if ($result) { Write-Host '[OK] DVP API is working'; Write-Host 'Projects found:' $result.Count } else { Write-Host '[ERROR] DVP API not responding' }"

echo.
echo Test complete!
pause
