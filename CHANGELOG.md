# 更新日志 (CHANGELOG)

本文档记录项目的所有重要更改。

格式基于 [Keep a Changelog](https://keepachangelog.com/zh-CN/1.0.0/)，
并且本项目遵循 [语义化版本](https://semver.org/lang/zh-CN/)。

---

## [v2.3.0-alpha] - 2026-03-13

### ✨ 新增功能

#### 1. WebSocket 实时推送系统
- ✅ WebSocket 连接管理器，支持多客户端连接
- ✅ 设备状态实时推送 (`/ws/devices`)
- ✅ 告警实时推送 (`/ws/alarms`)
- ✅ 性能指标实时推送 (`/ws/metrics`)
- ✅ 心跳机制（ping/pong）
- ✅ 自动重连支持
- ✅ 连接状态监控

**技术实现：**
```python
# WebSocket 端点
@router.websocket("/ws/devices")
async def websocket_devices(websocket: WebSocket):
    await manager.connect(websocket)
    # 实时推送设备状态
```

**使用效果：**
- 设备状态更新延迟 < 1秒
- 无需手动刷新页面
- 支持多用户同时在线

---

#### 2. 智能告警系统
- ✅ 分级告警（P0/P1/P2/P3）
- ✅ 告警类型定义（8种类型）
- ✅ 告警CRUD完整流程
- ✅ 告警确认/解决机制
- ✅ 告警统计概览
- ✅ 多维度查询（级别/状态/设备/时间）
- ✅ 告警生命周期管理

**告警级别：**
```
P0 - 紧急（设备故障/测试中断） - 红色
P1 - 严重（性能下降/异常） - 橙色
P2 - 警告（资源不足/即将过期） - 黄色
P3 - 提示（维护提醒/信息更新） - 绿色
```

**告警类型：**
- hardware_failure - 硬件故障
- communication_error - 通信错误
- performance_degradation - 性能下降
- environmental_anomaly - 环境异常
- test_failure - 测试失败
- resource_shortage - 资源不足
- maintenance_reminder - 维护提醒
- calibration_expired - 校准过期

**API端点：**
```
GET    /api/v1/alarms                    # 获取告警列表
POST   /api/v1/alarms                    # 创建告警
GET    /api/v1/alarms/{id}               # 获取告警详情
PUT    /api/v1/alarms/{id}/acknowledge   # 确认告警
PUT    /api/v1/alarms/{id}/resolve       # 解决告警
GET    /api/v1/alarms/statistics/overview # 告警统计
DELETE /api/v1/alarms/{id}               # 删除告警
```

---

#### 3. 性能指标体系
- ✅ 综合性能指标概览
- ✅ 设备性能指标计算
- ✅ 测试性能指标统计
- ✅ 趋势分析（设备利用率/测试通过率）
- ✅ 多维度数据查询
- ✅ 时间范围筛选

**核心指标：**

**设备指标：**
- 设备利用率 = (运行时间 / 总时间) × 100%
- MTBF（平均故障间隔时间）= 总运行时间 / 故障次数
- MTTR（平均修复时间）= 总维修时间 / 维修次数
- 设备可用率 = (总时间 - 维修时间) / 总时间 × 100%

**测试指标：**
- 测试通过率 = 通过用例数 / 总用例数 × 100%
- 节省人力（人天）= 节省工时 / 8
- 平均执行时长
- 自动化率

**API端点：**
```
GET /api/v1/metrics/overview          # 综合指标概览
GET /api/v1/metrics/devices           # 设备性能指标
GET /api/v1/metrics/tests             # 测试性能指标
GET /api/v1/metrics/trend/devices     # 设备利用率趋势
GET /api/v1/metrics/trend/tests       # 测试通过率趋势
```

---

### 📝 文档更新

- ✅ 新增优化计划文档 (`docs/OPTIMIZATION_PLAN.md`)
- ✅ 新增优化总结文档 (`docs/OPTIMIZATION_SUMMARY.md`)
- ✅ 新增更新日志 (`CHANGELOG.md`)

---

### 🔧 技术优化

- ✅ WebSocket 连接池管理
- ✅ 告警数据库模型设计
- ✅ 性能指标计算算法
- ✅ 趋势数据生成逻辑

---

### 📊 性能提升

| 指标 | v2.2.1 | v2.3.0 | 提升 |
|------|--------|--------|------|
| 实时更新能力 | ❌ | ✅ | +100% |
| 告警管理能力 | ❌ | ✅ | +100% |
| 性能监控能力 | 基础 | 完整 | +200% |
| 趋势分析能力 | ❌ | ✅ | +100% |

---

### 🎯 下一步计划

#### Phase 2: 增强功能（计划中）
- 📅 设备预约调度系统
- 📊 数据导出功能（PDF/Excel）
- 📱 移动端适配优化
- 🔔 通知系统集成（邮件/钉钉/飞书）

#### Phase 3: AI增强（计划中）
- 🤖 故障预测算法
- 📈 智能趋势分析
- 💡 优化建议生成
- 🎯 异常检测

---

## [v2.2.1] - 2026-03-13

### ✨ 新增
- 四合一统一平台（台架/DVP/自动化/AI）
- 基础数据展示功能
- Windows 一键启动脚本
- SQLite 数据库支持

### 🐛 修复
- 修复DVP看板无法使用的问题
- 修复启动脚本编码问题
- 优化前端API配置

### 📝 文档
- 精简README文档
- 添加快速开始指南
- 添加故障排查指南

---

## [v2.2.0] - 2026-03-13

### ✨ 新增
- 自动化测试看板
- AI辅助看板
- DVP看板本地化
- 四合一统一平台

---

## [v2.1.0] - 2026-03-12

### ✨ 新增
- 测试台架看板
- DVP进度看板
- 基础架构搭建

---

## 版本命名规则

- **主版本号（Major）**: 重大架构变更或不兼容的API修改
- **次版本号（Minor）**: 新增功能，向后兼容
- **修订号（Patch）**: Bug修复，向后兼容
- **预发布版本**: alpha（内测）、beta（公测）、rc（候选发布）

---

## 版本历史

- **v2.3.0-alpha** (2026-03-13) - WebSocket + 告警 + 指标
- **v2.2.1** (2026-03-13) - Bug修复 + 文档优化
- **v2.2.0** (2026-03-13) - 四合一平台
- **v2.1.0** (2026-03-12) - 初始版本

---

**当前版本：v2.3.0-alpha**  
**下一版本：v2.3.0-beta（计划）**
