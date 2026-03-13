@echo off
echo ========================================
echo   统一看板平台 - 全部服务启动
echo ========================================
echo.

REM 检查 Python
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python not found. Please install Python 3.10+
    pause
    exit /b 1
)

REM 检查 Node.js
node --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Node.js not found. Please install Node.js 18+
    pause
    exit /b 1
)

echo [INFO] 正在启动所有服务...
echo.

REM ========================================
REM 1. 启动测试台架后端
REM ========================================
echo [1/3] 启动测试台架后端服务...
start "Test Bench Backend" cmd /k "cd /d %~dp0backend && start.bat"
timeout /t 3 /nobreak >nul

REM ========================================
REM 2. 启动DVP后端
REM ========================================
echo [2/3] 启动DVP后端服务...
cd /d %~dp0..\dvp-dashboard\backend
if exist start.bat (
    start "DVP Backend" cmd /k "start.bat"
    timeout /t 3 /nobreak >nul
) else (
    echo [WARNING] DVP backend not found, skipping...
)

REM ========================================
REM 3. 启动前端服务
REM ========================================
echo [3/3] 启动前端服务...
cd /d %~dp0frontend

REM 检查是否需要安装 serve
npm list -g serve >nul 2>&1
if errorlevel 1 (
    echo [INFO] Installing serve for frontend...
    npm install -g serve
)

echo.
echo ========================================
echo   所有服务启动完成！
echo ========================================
echo.
echo [INFO] 访问地址：
echo   - 前端看板:     http://192.168.1.100:3000
echo   - 测试台架API:  http://192.168.1.100:8000
echo   - DVP API:      http://192.168.1.100:8001
echo.
echo [INFO] API 文档：
echo   - 测试台架:     http://192.168.1.100:8000/docs
echo   - DVP:          http://192.168.1.100:8001/docs
echo.
echo [INFO] 按 Ctrl+C 停止前端服务
echo ========================================
echo.

serve -s out -l 3000

pause
