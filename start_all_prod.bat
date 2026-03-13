@echo off
chcp 65001 >nul
echo ========================================
echo   统一看板平台 - 生产模式启动
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

echo [INFO] 正在启动所有服务（生产模式）...
echo.

REM ========================================
REM 1. 启动后端服务
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
REM 3. 启动前端（生产模式）
REM ========================================
echo [3/3] 启动前端生产服务器...
cd /d %~dp0frontend

REM 检查是否需要安装 serve
npm list -g serve >nul 2>&1
if errorlevel 1 (
    echo [INFO] 正在安装 serve...
    npm install -g serve
)

REM 检查构建是否存在
if not exist "out\index.html" (
    echo [WARNING] 未找到构建文件，正在构建...
    call npm run build
)

echo.
echo ========================================
echo   所有服务启动完成！
echo ========================================
echo.
echo [INFO] 访问地址：
echo   - 前端看板:     http://localhost:3000
echo   - 后端API:      http://localhost:8000
echo.
echo [INFO] 局域网访问：
echo   - 前端看板:     http://192.168.1.100:3000
echo   - 后端API:      http://192.168.1.100:8000
echo.
echo [INFO] API 文档：
echo   - Swagger UI:   http://localhost:8000/docs
echo   - ReDoc:        http://localhost:8000/redoc
echo.
echo [INFO] 按 Ctrl+C 停止前端服务
echo ========================================
echo.

serve -s out -l 3000

pause
