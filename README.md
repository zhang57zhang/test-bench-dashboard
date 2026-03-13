# 智能测试台架工厂数字孪生看板

[![License](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Version](https://img.shields.io/badge/version-2.2.0-blue.svg)](https://github.com/zhang57zhang/test-bench-dashboard)
[![Next.js](https://img.shields.io/badge/Next.js-14.2.20-green.svg)](https://nextjs.org/)
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
- ✅ **实时监控** - 设备状态、项目进度、测试执行实时更新
- ✅ **数据可视化** - 直观的图表和统计数据展示
- ✅ **多维度统计** - 按天/周/月/年/项目多维度分析
- ✅ **科技感UI** - 现代化的用户界面设计
- ✅ **Windows优化** - 专为Windows平台优化的一键启动脚本

---

## 🚀 快速开始

### 娡式1：一键启动（推荐）

**Windows系统：**
```bash
双击运行：start_all.bat
```

**Mac/Linux系统：**
```bash
chmod +x start_all.sh
./start_all.sh
```

### 模式2：开发模式

**Windows:**
```bash
双击运行：start_all_dev.bat
```

**Mac/Linux:**
```bash
./start_all_dev.sh
```

### 模式3：生产模式

**Windows:**
```bash
双击运行：start_all_prod.bat
```

**Mac/Linux:**
```bash
./start_all_prod.sh
```

---

## 📱 访问地址

启动成功后访问：

- **前端看板：** http://localhost:3000 或 http://192.168.1.100:3000
- **后端API：** http://localhost:8000
- **API文档：** http://localhost:8000/docs

---

## 🎯 功能模块

### 1. 🏭 测试台架看板

**功能：**
- 实时设备状态监控
- 5分钟心跳检测间隔
- 设备在线/离线/维护/告警状态
- 实验室管理
- 位置可视化编辑
- 告警系统

**技术实现：**
- 设备监控服务：`backend/app/core/device_monitor.py`
- 自动ping检测
- 动态配置支持

**API端点：**
- `GET /api/v1/benches` - 获取设备列表
- `GET /api/v1/benches/{id}` - 获取设备详情
- `POST /api/v1/benches` - 创建设备
- `PUT /api/v1/benches/{id}` - 更新设备
- `DELETE /api/v1/benches/{id}` - 删除设备

---

### 2. 📊 DVP进度看板

**功能：**
- 项目进度跟踪
- 实验组管理
- 设备状态监控
- 统计数据展示

**技术实现：**
- 完全本地化实现：`backend/app/api/dvp.py`
- 内存数据存储 + 文件持久化
- 无外部依赖

**API端点:**
- `GET /api/v1/dvp/projects` - 获取项目列表
- `GET /api/v1/dvp/statistics` - 获取统计信息
- `POST /api/v1/dvp/projects/generate` - 重新生成模拟数据

---

### 3. 🤖 自动化测试看板

**功能：**
- 总用例数统计
- 执行时长统计
- 节省人力计算（人天，按8小时/天）
- 通过率分析
- 多维度统计（天/周/月/年）
- 按项目维度统计
- 趋势图表展示

**技术实现:**
- API实现：`backend/app/api/automation.py`
- 前端组件：`frontend/src/components/AutomationDashboard.tsx`

**API端点：**
- `GET /api/v1/automation/metrics` - 获取完整指标
- `GET /api/v1/automation/overview` - 获取总览数据
- `GET /api/v1/automation/by-project` - 按项目统计
- `GET /api/v1/automation/by-period` - 按时间周期统计

**统计维度：**
- 总用例数
- 总执行时长（小时）
- 节省人力（人天）
- 通过率
- 活跃项目数

---

### 4. 🧠 AI辅助看板

**功能:**
- 11种AI辅助活动统计
- 总辅助次数统计
- 节省人力计算（人天，按8小时/天）
- 活动类型占比分析
- Top 5活动展示
- 趋势图表展示

**技术实现:**
- API实现：`backend/app/api/ai_assistant.py`
- 前端组件：`frontend/src/components/AIAssistantDashboard.tsx`

**API端点:**
- `GET /api/v1/ai-assistant/metrics` - 获取完整指标
- `GET /api/v1/ai-assistant/overview` - 获取总览数据
- `GET /api/v1/ai-assistant/by-activity` - 按活动类型统计
- `GET /api/v1/ai-assistant/by-period` - 按时间周期统计

**11种AI辅助活动:**
1. 需求分析
2. 测试策略
3. 测试设计
4. 用例编写
5. 用例审查
6. 脚本编写
7. 脚本调试
8. 脚本执行
9. 日志分析
10. 数据分析
11. 报告编写

---

## 🏗️ 技术栈

### 后端

- **框架：** FastAPI 0.115.0
- **语言：** Python 3.10+
- **数据库：** SQLite (默认) / PostgreSQL (可选)
- **验证：** Pydantic 2.9.2
- **异步：** asyncio

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
│   │   │   ├── benches.py      # 测试台架API
│   │   │   ├── dvp.py          # DVP进度API
│   │   │   ├── automation.py   # 自动化测试API
│   │   │   └── ai_assistant.py # AI辅助API
│   │   ├── core/               # 核心模块
│   │   ├── models/             # 数据模型
│   │   └── main.py             # 应用入口
│   ├── start.bat               # Windows启动脚本
│   └── requirements.txt        # Python依赖
│
├── frontend/                   # 前端服务
│   ├── src/
│   │   ├── app/                # 页面
│   │   ├── components/         # React组件
│   │   ├── lib/                # 工具库
│   │   ├── store/              # 状态管理
│   │   └── types/              # 类型定义
│   ├── public/                 # 静态资源
│   ├── package.json            # Node.js依赖
│   └── next.config.js          # Next.js配置
│
├── start_all.bat               # 一键启动（Windows）
├── start_all_dev.bat           # 开发模式启动（Windows）
├── start_all_prod.bat          # 生产模式启动（Windows）
├── README.md                   # 项目文档
└── QUICKSTART.md               # 快速开始指南
```

---

## ⚙️ 配置说明

### 前端配置

**文件位置：** `frontend/public/config.json`

```json
{
  "apiUrl": "http://192.168.1.100:8000/api/v1",
  "dvpApiUrl": "http://192.168.1.100:8001",
  "version": "2.2.0",
  "features": {
    "testBenchDashboard": true,
    "dvpDashboard": true,
    "automationDashboard": true,
    "aiAssistantDashboard": true
  }
}
```

### 后端配置

**文件位置：** `backend/.env`

```bash
DEBUG=True
HOST=0.0.0.0
PORT=8000
```

---

## 🔧 开发指南

### 环境要求

- Python 3.10+
- Node.js 18+
- npm 或 yarn

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
source venv/bin/activate  # Mac/Linux
pip install -r requirements.txt
python main.py
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

## 📚 文档

- **快速开始：** `QUICKSTART.md`
- **部署指南：** `DEPLOYMENT_GUIDE.md`
- **启动指南：** `STARTUP_GUIDE.md`
- **错误修复：** `TROUBLESHOOTING.md`
- **多看板指南：** `MULTI_DASHBOARD_GUIDE.md`

---

## 🐛 故障排查

### 常见问题

**1. 端口被占用**
```bash
# Windows
netstat -ano | findstr :3000
taskkill /F /PID <PID>
```

**2. Python未找到**
- 下载安装 Python 3.10+
- 添加到系统PATH

**3. Node.js未找到**
- 下载安装 Node.js 18+
- 添加到系统PATH

**4. 构建错误**
```bash
# 运行清理和重建脚本
双击运行：clean_and_rebuild.bat
```

详细故障排查请查看 `TROUBLESHOOTING.md`

---

## 📊 性能指标

- **页面加载：** < 2秒
- **API响应：** < 500ms
- **数据刷新：** 5分钟间隔
- **静态资源：** ~120KB

---

## 🔄 更新日志

### v2.2.0 (2026-03-13)

**新增功能：**
- ✅ 自动化测试看板
- ✅ AI辅助看板
- ✅ DVP看板完全本地化
- ✅ 三种启动方式

**改进：**
- ✅ Windows启动脚本优化
- ✅ 单服务架构（端口8000）
- ✅ 移除所有外部依赖

**修复：**
- ✅ Next.js Hydration Error
- ✅ 模块找不到错误
- ✅ 编码问题

### v2.1.0 (2026-03-12)

- 初始版本
- 测试台架看板
- DVP进度看板

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

**维护团队：** OpenClaw AI Assistant  
**当前版本：** v2.2.0  
**最后更新：** 2026-03-13
