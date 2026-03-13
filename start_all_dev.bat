@echo off
chcp 65001 >nul
echo ========================================
echo   统一看板平台 - 开发模式启动
echo ========================================
echo.

REM 检查 Python
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] 未找到 Python。请安装 Python 3.10+
    pause
    exit /b 1
)

REM 检查 Node.js
node --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] 未找到 Node.js。请安装 Node.js 18+
    pause
    exit /b 1
)

echo [INFO] 正在启动所有服务（开发模式）...
echo.

REM ========================================
REM 1. 启动测试台架后端
REM ========================================
echo [1/3] 启动后端服务...
start "Backend Server" cmd /k "cd /d %~dp0backend && start.bat"
timeout /t 5 /nobreak >nul

REM ========================================
REM 2. DVP已本地化
REM ========================================
echo [2/3] DVP后端已本地化到主后端
timeout /t 1 /nobreak >nul

REM ========================================
REM 3. 启动前端（开发模式）
REM ========================================
echo [3/3] 启动前端开发服务器...
cd /d %~dp0frontend

echo.
echo ========================================
echo   所有服务启动完成！
echo ========================================
echo.
echo [INFO] 访问地址：
echo   - 前端看板:     http://localhost:3000
echo   - 后端API:      http://localhost:8000
echo.
echo [INFO] API 文档：
echo   - Swagger UI:   http://localhost:8000/docs
echo.
echo [INFO] 按 Ctrl+C 停止前端服务
echo ========================================
echo.

npm run dev

pause
