@echo off
echo ========================================
echo   DVP看板测试和修复
echo ========================================
echo.

REM 启动后端
echo [1/3] 启动后端服务...
start "Backend Server" cmd /k "cd /d %~dp0backend && start.bat"

REM 等待后端启动
timeout /t 10 /nobreak >nul

REM 测试后端API
echo [2/3] 测试后端API...
curl -s http://localhost:8000/health >nul 2>&1
if errorlevel 1 (
    echo [ERROR] 后端API无法访问
    echo 请检查后端是否正常启动
    pause
    exit /b 1
) else (
    echo [OK] 后端API正常
)

REM 测试DVP API
echo [3/3] 测试DVP API...
curl -s http://localhost:8000/api/v1/dvp/projects >nul 2>&1
if errorlevel 1 (
    echo [ERROR] DVP API无法访问
    echo 请检查DVP路由是否正确配置
    pause
    exit /b 1
) else (
    echo [OK] DVP API正常
)

echo.
echo ========================================
echo   测试完成！
echo ========================================
echo.
echo [INFO] 后端服务运行在: http://localhost:8000
echo [INFO] API文档地址: http://localhost:8000/docs
echo [INFO] DVP API地址: http://localhost:8000/api/v1/dvp/projects
echo.
pause
