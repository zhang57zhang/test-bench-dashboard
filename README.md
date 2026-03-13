# 智能测试台架工厂数字孪生看板

[![License](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Version](https://img.shields.io/badge/version-2.3.0--alpha-blue.svg)](https://github.com/zhang57zhang/test-bench-dashboard)
[![Next.js](https://img.shields.io/badge/Next.js-14.2.20-black.svg)](https://nextjs.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115.0-green.svg)](https://fastapi.tiangolo.com/)

**统一的四合一测试全流程监控平台**

---

## 📖 项目简介

智能测试台架工厂数字孪生看板是一个统一的测试全流程监控平台，整合了：
- 🏭 **测试台架看板** - 实时设备监控与数字孪生
- 📊 **DVP进度看板** - 项目进度跟踪与管理
- 🤖 **自动化测试看板** - 自动化测试执行统计
- 🧠 **AI辅助看板** - AI辅助活动统计分析

### ✨ 核心特性

- ✅ **四合一统一平台** - 一个平台管理所有测试相关看板
- ✅ **WebSocket实时推送** ⭐ NEW - 设备状态、告警、指标实时更新
- ✅ **智能告警系统** ⭐ NEW - 分级告警（P0-P3）+ 完整生命周期管理
- ✅ **性能指标体系** ⭐ NEW - 设备利用率、MTBF、MTTR、测试通过率等
- ✅ **趋势分析** ⭐ NEW - 多维度趋势图表，辅助决策
- ✅ **数据可视化** - 直观的图表和统计数据展示
- ✅ **多维度统计** - 按天/周/月/年/项目多维度分析
- ✅ **科技感UI** - 现代化的用户界面设计
- ✅ **Windows优化** - 专为Windows平台优化的一键启动

---

## 🚀 快速开始（5分钟上手）

### 方式1：一键启动（推荐）⭐

**Windows系统：**
```bash
双击运行：start_all_fixed.bat
```

等待15-20秒，浏览器会自动打开 http://localhost:3000

### 方式2：开发模式

**Windows系统：**
```bash
双击运行：start_all_dev.bat
```

### 方式3：手动启动

**启动后端：**
```bash
cd backend
start.bat
```

**启动前端（新终端）：**
```bash
cd frontend
serve -s out -l 3000
```

**访问：** http://localhost:3000

---

## 📱 访问地址

启动成功后访问：

- **前端看板：** http://localhost:3000
- **后端API：** http://localhost:8000
- **API文档：** http://localhost:8000/docs

---

## 🎯 功能模块

### 1. 🏭 测试台架看板

**功能：**
- 实时设备状态监控（在线/离线/维护/告警）
- 5分钟心跳检测间隔
- 实验室管理
- 位置可视化编辑
- 告警系统

**API端点：**
- `GET /api/v1/benches` - 获取设备列表
- `POST /api/v1/benches` - 创建设备
- `PUT /api/v1/benches/{id}` - 更新设备

---

### 2. 📊 DVP进度看板

**功能：**
- 项目进度跟踪
- 实验组管理
- 设备状态监控
- 统计数据展示（总项目、进行中、已完成、已中断）

**API端点：**
- `GET /api/v1/dvp/projects` - 获取项目列表
- `GET /api/v1/dvp/statistics` - 获取统计信息

---

### 3. 🤖 自动化测试看板

**功能：**
- 总用例数统计
- 执行时长统计
- 节省人力计算（人天，按8小时/天）
- 通过率分析
- 多维度统计（天/周/月/年）
- 按项目维度统计

**API端点：**
- `GET /api/v1/automation/metrics` - 获取完整指标
- `GET /api/v1/automation/overview` - 获取总览数据

---

### 4. 🧠 AI辅助看板

**功能：**
- 11种AI辅助活动统计
- 总辅助次数统计
- 节省人力计算（人天，按8小时/天）
- 活动类型占比分析
- Top 5活动展示

**11种AI辅助活动：**
需求分析、测试策略、测试设计、用例编写、用例审查、
脚本编写、脚本调试、脚本执行、日志分析、数据分析、报告编写

**API端点：**
- `GET /api/v1/ai-assistant/metrics` - 获取完整指标
- `GET /api/v1/ai-assistant/by-activity` - 按活动类型统计

---

## 🏗️ 技术栈

### 后端
- **框架：** FastAPI 0.115.0
- **语言：** Python 3.10+
- **数据库：** SQLite (默认)
- **验证：** Pydantic 2.9.2

### 前端
- **框架：** Next.js 14.2.20
- **语言：** TypeScript
- **UI库：** Tailwind CSS
- **状态管理：** Zustand
- **HTTP客户端：** Axios

---

## 📁 项目结构

```
test_bench_dashboard/
├── backend/                    # 后端服务
│   ├── app/
│   │   ├── api/                # API路由
│   │   ├── core/               # 核心模块
│   │   ├── models/             # 数据模型
│   │   └── main.py             # 应用入口
│   └── start.bat               # 启动脚本
│
├── frontend/                   # 前端服务
│   ├── src/
│   │   ├── app/                # 页面
│   │   ├── components/         # React组件
│   │   ├── lib/                # 工具库
│   │   └── types/              # 类型定义
│   └── public/                 # 静态资源
│
├── start_all_fixed.bat         # 一键启动（推荐）
├── start_all_dev.bat           # 开发模式启动
├── test_dvp_quick.bat          # 快速测试
├── README.md                   # 项目文档
├── QUICKSTART.md               # 快速开始
└── DEPLOYMENT_GUIDE.md         # 部署指南
```

---

## 🔧 开发指南

### 环境要求

- Python 3.10+
- Node.js 18+

### 本地开发

**1. 克隆项目**
```bash
git clone https://github.com/zhang57zhang/test-bench-dashboard.git
cd test-bench-dashboard
```

**2. 启动后端**
```bash
cd backend
python -m venv venv
venv\Scripts\activate  # Windows
pip install -r requirements.txt
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**3. 启动前端（新终端）**
```bash
cd frontend
npm install
npm run dev
```

**4. 访问应用**
- 前端：http://localhost:3000
- 后端：http://localhost:8000
- API文档：http://localhost:8000/docs

---

## 🐛 故障排查

### 问题1：端口被占用

**解决方案：**
```bash
# Windows
netstat -ano | findstr :3000
taskkill /F /PID <PID>
```

### 问题2：服务未启动

**解决方案：**
```bash
# 使用一键启动脚本
双击运行：start_all_fixed.bat
```

### 问题3：看板无法访问

**检查步骤：**
1. 确认后端已启动（访问 http://localhost:8000/health）
2. 确认前端已启动（访问 http://localhost:3000）
3. 查看浏览器控制台错误

**快速测试：**
```bash
双击运行：test_dvp_quick.bat
```

---

## 📚 文档

- **快速开始：** `QUICKSTART.md`
- **部署指南：** `DEPLOYMENT_GUIDE.md`
- **故障排查：** `TROUBLESHOOTING.md`

---

## 🔄 更新日志

### v2.2.1 (2026-03-13)

**修复：**
- ✅ 修复DVP看板无法使用的问题
- ✅ 修复启动脚本编码问题
- ✅ 优化前端API配置
- ✅ 清理过程文件

**改进：**
- ✅ 简化启动流程
- ✅ 精简文档结构
- ✅ 优化用户体验

### v2.2.0 (2026-03-13)

**新增功能：**
- ✅ 自动化测试看板
- ✅ AI辅助看板
- ✅ DVP看板完全本地化
- ✅ 四合一统一平台

### v2.1.0 (2026-03-12)

- 初始版本
- 测试台架看板
- DVP进度看板

---

## 📊 性能指标

- **页面加载：** < 2秒
- **API响应：** < 500ms
- **数据刷新：** 5分钟间隔
- **静态资源：** ~120KB

---

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

---

## 📄 许可证

[MIT License](LICENSE)

---

## 📞 联系方式

- **GitHub:** https://github.com/zhang57zhang/test-bench-dashboard
- **问题反馈：** 提交 GitHub Issue

---

**当前版本：** v2.2.1  
**最后更新：** 2026-03-13  
**维护团队：** OpenClaw AI Assistant
