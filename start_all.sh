#!/bin/bash

echo "========================================"
echo "  统一看板平台 - 全部服务启动"
echo "========================================"
echo ""

# 检查 Python
if ! command -v python3 &> /dev/null; then
    echo "[ERROR] Python3 not found. Please install Python 3.10+"
    exit 1
fi

# 检查 Node.js
if ! command -v node &> /dev/null; then
    echo "[ERROR] Node.js not found. Please install Node.js 18+"
    exit 1
fi

echo "[INFO] 正在启动所有服务..."
echo ""

# ========================================
# 1. 启动测试台架后端
# ========================================
echo "[1/3] 启动测试台架后端服务..."
cd backend
osascript -e 'tell application "Terminal" to do script "cd \"'$(pwd)'\" && ./start.sh"'
cd ..
sleep 3

# ========================================
# 2. 启动DVP后端
# ========================================
echo "[2/3] 启动DVP后端服务..."
if [ -d "../dvp-dashboard/backend" ]; then
    cd ../dvp-dashboard/backend
    osascript -e 'tell application "Terminal" to do script "cd \"'$(pwd)'\" && ./start.sh"'
    cd ../../test_bench_dashboard
    sleep 3
else
    echo "[WARNING] DVP backend not found, skipping..."
fi

# ========================================
# 3. 启动前端服务
# ========================================
echo "[3/3] 启动前端服务..."
cd frontend

# 检查是否需要安装 serve
if ! command -v serve &> /dev/null; then
    echo "[INFO] Installing serve for frontend..."
    npm install -g serve
fi

echo ""
echo "========================================"
echo "  所有服务启动完成！"
echo "========================================"
echo ""
echo "[INFO] 访问地址："
echo "  - 前端看板:     http://192.168.1.100:3000"
echo "  - 测试台架API:  http://192.168.1.100:8000"
echo "  - DVP API:      http://192.168.1.100:8001"
echo ""
echo "[INFO] API 文档："
echo "  - 测试台架:     http://192.168.1.100:8000/docs"
echo "  - DVP:          http://192.168.1.100:8001/docs"
echo ""
echo "[INFO] 按 Ctrl+C 停止前端服务"
echo "========================================"
echo ""

serve -s out -l 3000
