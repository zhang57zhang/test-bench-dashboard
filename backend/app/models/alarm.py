"""
Alarm Model
告警数据模型
"""

from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.sql import func
from app.core.database import Base


class Alarm(Base):
    """告警表"""
    __tablename__ = "alarms"
    
    id = Column(Integer, primary_key=True, index=True)
    device_id = Column(Integer, ForeignKey("devices.id"), nullable=True)
    level = Column(String(2), nullable=False)  # P0/P1/P2/P3
    type = Column(String(50), nullable=False)  # 告警类型
    message = Column(Text, nullable=False)  # 告警消息
    status = Column(String(20), default="active")  # active/resolved/acknowledged
    acknowledged_by = Column(String(100), nullable=True)  # 确认人
    resolved_at = Column(DateTime(timezone=True), nullable=True)  # 解决时间
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    def to_dict(self):
        """转换为字典"""
        return {
            "id": self.id,
            "device_id": self.device_id,
            "level": self.level,
            "type": self.type,
            "message": self.message,
            "status": self.status,
            "acknowledged_by": self.acknowledged_by,
            "resolved_at": self.resolved_at.isoformat() if self.resolved_at else None,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }


# 告警级别定义
ALARM_LEVELS = {
    "P0": {
        "name": "紧急",
        "color": "#F5222D",
        "description": "设备故障/测试中断",
        "notification": ["email", "dingtalk", "feishu", "sms"]
    },
    "P1": {
        "name": "严重",
        "color": "#FA8C16",
        "description": "性能下降/异常",
        "notification": ["email", "dingtalk", "feishu"]
    },
    "P2": {
        "name": "警告",
        "color": "#FAAD14",
        "description": "资源不足/即将过期",
        "notification": ["email", "dingtalk"]
    },
    "P3": {
        "name": "提示",
        "color": "#52C41A",
        "description": "维护提醒/信息更新",
        "notification": ["dingtalk"]
    }
}

# 告警类型定义
ALARM_TYPES = {
    "hardware_failure": "硬件故障",
    "communication_error": "通信错误",
    "performance_degradation": "性能下降",
    "environmental_anomaly": "环境异常",
    "test_failure": "测试失败",
    "resource_shortage": "资源不足",
    "maintenance_reminder": "维护提醒",
    "calibration_expired": "校准过期"
}
