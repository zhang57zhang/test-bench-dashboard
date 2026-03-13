# 🚀 Windows 启动脚本使用指南

## 问题修复

### ❌ 原始问题
- 编码错误：中文字符无法正确显示
- 语法错误：某些命令被当作文件名执行
- DVP后端：不需要单独启动（已本地化）

### ✅ 已修复
- 使用正确的编码（UTF-8 with BOM）
- 简化启动流程
- 移除DVP后端单独启动步骤

---

## 📁 启动脚本说明

### 1. start_all.bat（推荐）
**用途：** 一键启动所有服务（开发+生产混合模式）

**特点：**
- ✅ 自动启动后端（开发模式）
- ✅ 自动启动前端（生产模式）
- ✅ DVP已本地化，无需单独启动
- ✅ 自动安装依赖
- ✅ 自动构建前端

**使用方法：**
```bash
双击运行：start_all.bat
```

**启动后访问：**
- 前端：http://localhost:3000 或 http://192.168.1.100:3000
- 后端API：http://localhost:8000
- API文档：http://localhost:8000/docs

---

### 2. start_all_dev.bat
**用途：** 开发模式启动

**特点：**
- 后端：开发模式（自动重载）
- 前端：开发模式（热重载）
- 适合开发调试

**使用方法：**
```bash
双击运行：start_all_dev.bat
```

---

### 3. start_all_prod.bat
**用途：** 生产模式启动

**特点：**
- 后端：生产模式
- 前端：静态文件服务
- 适合生产部署

**使用方法：**
```bash
双击运行：start_all_prod.bat
```

---

## 🔧 手动启动方式

### 方式1：分别启动（推荐新手）

**步骤1：启动后端**
```bash
cd backend
start.bat
```

**步骤2：启动前端（新终端）**
```bash
cd frontend
npm run dev
```

**访问：** http://localhost:3000

---

### 方式2：生产模式启动

**步骤1：构建前端**
```bash
cd frontend
npm run build
```

**步骤2：启动后端**
```bash
cd backend
python main.py
```

**步骤3：启动前端**
```bash
cd frontend
serve -s out -l 3000
```

---

## 📊 服务架构

```
start_all.bat
    ↓
[后端服务] 端口 8000
    ├─ 测试台架API /api/v1/benches
    ├─ DVP API /api/v1/dvp (本地化)
    ├─ 自动化API /api/v1/automation
    └─ AI辅助API /api/v1/ai-assistant
    
[前端服务] 端口 3000
    ├─ 测试台架看板
    ├─ DVP进度看板
    ├─ 自动化测试看板
    └─ AI辅助看板
```

---

## ⚠️ 匜见问题

### 问题1：端口被占用

**错误信息：**
```
Error: listen EADDRINUSE: address already in use :::3000
```

**解决方案：**
```bash
# 查找占用端口的进程
netstat -ano | findstr :3000
netstat -ano | findstr :8000

# 结束进程（替换PID为实际进程ID）
taskkill /F /PID <PID>
```

---

### 问题2：Python未找到

**错误信息：**
```
[ERROR] 未找到 Python
```

**解决方案：**
1. 下载安装 Python 3.10+
2. 添加到系统PATH
3. 重启命令行

---

### 问题3：Node.js未找到

**错误信息：**
```
[ERROR] 未找到 Node.js
```

**解决方案：**
1. 下载安装 Node.js 18+
2. 添加到系统PATH
3. 重启命令行

---

### 问题4：serve命令未找到

**错误信息：**
```
'serve' 不是内部或外部命令
```

**解决方案：**
```bash
# 自动安装（脚本会自动执行）
npm install -g serve

# 手动安装
npm install -g serve
```

---

## ✅ 验证启动成功

### 检查后端
```bash
# 方式1：浏览器访问
http://localhost:8000/health

# 方式2：命令行
curl http://localhost:8000/health

# 预期返回
{"status": "healthy"}
```

### 检查前端
```bash
# 浏览器访问
http://localhost:3000

# 应该看到看板界面
```

### 检查所有看板
1. 访问 http://localhost:3000
2. 点击顶部看板选择器
3. 依次切换四个看板
4. 确认都能正常显示

---

## 🎯 推荐使用方式

### 开发调试
```bash
使用：start_all_dev.bat
```
- 后端自动重载
- 前端热重载
- 方便调试

### 生产部署
```bash
使用：start_all_prod.bat
```
- 性能更好
- 更稳定
- 适合长期运行

### 快速演示
```bash
使用：start_all.bat
```
- 一键启动
- 自动化程度高
- 适合演示

---

## 📝 注意事项

1. **首次启动**
   - 需要等待依赖安装
   - 需要等待前端构建
   - 总耗时约2-3分钟

2. **后续启动**
   - 依赖已安装，启动更快
   - 约30秒即可完成

3. **停止服务**
   - 按 Ctrl+C 停止前端
   - 关闭后端窗口

4. **重启服务**
   - 先停止所有服务
   - 再重新启动

---

## 🔗 相关文档

- **快速开始：** `QUICKSTART.md`
- **部署指南：** `DEPLOYMENT_GUIDE.md`
- **错误修复：** `TROUBLESHOOTING.md`
- **多看板指南：** `MULTI_DASHBOARD_GUIDE.md`

---

**最后更新：** 2026-03-13  
**维护团队：** OpenClaw AI Assistant
