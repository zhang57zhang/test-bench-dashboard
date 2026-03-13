"""
Alarms API V2
智能告警系统 API
"""

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
import sqlite3
from app.core.database import get_db_connection
from app.models.alarm import ALARM_LEVELS, ALARM_TYPES

router = APIRouter(prefix="/api/v1/alarms", tags=["alarms"])


# Pydantic 模型
class AlarmCreate(BaseModel):
    """创建告警"""
    device_id: Optional[int] = None
    level: str = Field(..., regex="^(P0|P1|P2|P3)$")
    type: str
    message: str


class AlarmAcknowledge(BaseModel):
    """确认告警"""
    acknowledged_by: str


class AlarmResolve(BaseModel):
    """解决告警"""
    resolved_note: Optional[str] = None


class AlarmResponse(BaseModel):
    """告警响应"""
    id: int
    device_id: Optional[int]
    level: str
    type: str
    message: str
    status: str
    acknowledged_by: Optional[str]
    resolved_at: Optional[datetime]
    created_at: datetime
    updated_at: Optional[datetime]


# API 端点
@router.get("/", response_model=List[AlarmResponse])
async def get_alarms(
    level: Optional[str] = Query(None, regex="^(P0|P1|P2|P3)$"),
    status: Optional[str] = Query(None, regex="^(active|resolved|acknowledged)$"),
    device_id: Optional[int] = None,
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0)
):
    """
    获取告警列表
    
    参数：
    - level: 告警级别 (P0/P1/P2/P3)
    - status: 告警状态 (active/resolved/acknowledged)
    - device_id: 设备ID
    - limit: 返回数量
    - offset: 偏移量
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # 构建查询
    query = "SELECT * FROM alarms WHERE 1=1"
    params = []
    
    if level:
        query += " AND level = ?"
        params.append(level)
    
    if status:
        query += " AND status = ?"
        params.append(status)
    
    if device_id:
        query += " AND device_id = ?"
        params.append(device_id)
    
    query += " ORDER BY created_at DESC LIMIT ? OFFSET ?"
    params.extend([limit, offset])
    
    cursor.execute(query, params)
    rows = cursor.fetchall()
    conn.close()
    
    alarms = []
    for row in rows:
        alarms.append(AlarmResponse(
            id=row['id'],
            device_id=row['device_id'],
            level=row['level'],
            type=row['type'],
            message=row['message'],
            status=row['status'],
            acknowledged_by=row['acknowledged_by'],
            resolved_at=row['resolved_at'],
            created_at=row['created_at'],
            updated_at=row['updated_at']
        ))
    
    return alarms


@router.post("/", response_model=AlarmResponse)
async def create_alarm(alarm: AlarmCreate):
    """
    创建告警
    
    自动触发通知（根据告警级别）
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # 插入告警
    cursor.execute("""
        INSERT INTO alarms (device_id, level, type, message, status, created_at)
        VALUES (?, ?, ?, ?, 'active', ?)
    """, (alarm.device_id, alarm.level, alarm.type, alarm.message, datetime.now()))
    
    alarm_id = cursor.lastrowid
    conn.commit()
    
    # 获取创建的告警
    cursor.execute("SELECT * FROM alarms WHERE id = ?", (alarm_id,))
    row = cursor.fetchone()
    conn.close()
    
    # TODO: 触发通知（邮件/钉钉/飞书）
    # await send_alarm_notification(alarm)
    
    return AlarmResponse(
        id=row['id'],
        device_id=row['device_id'],
        level=row['level'],
        type=row['type'],
        message=row['message'],
        status=row['status'],
        acknowledged_by=row['acknowledged_by'],
        resolved_at=row['resolved_at'],
        created_at=row['created_at'],
        updated_at=row['updated_at']
    )


@router.get("/{alarm_id}", response_model=AlarmResponse)
async def get_alarm(alarm_id: int):
    """获取单个告警详情"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM alarms WHERE id = ?", (alarm_id,))
    row = cursor.fetchone()
    conn.close()
    
    if not row:
        raise HTTPException(status_code=404, detail="Alarm not found")
    
    return AlarmResponse(
        id=row['id'],
        device_id=row['device_id'],
        level=row['level'],
        type=row['type'],
        message=row['message'],
        status=row['status'],
        acknowledged_by=row['acknowledged_by'],
        resolved_at=row['resolved_at'],
        created_at=row['created_at'],
        updated_at=row['updated_at']
    )


@router.put("/{alarm_id}/acknowledge")
async def acknowledge_alarm(alarm_id: int, ack: AlarmAcknowledge):
    """
    确认告警
    
    标记告警已被确认，状态变为 acknowledged
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # 检查告警是否存在
    cursor.execute("SELECT * FROM alarms WHERE id = ?", (alarm_id,))
    row = cursor.fetchone()
    
    if not row:
        conn.close()
        raise HTTPException(status_code=404, detail="Alarm not found")
    
    # 更新状态
    cursor.execute("""
        UPDATE alarms 
        SET status = 'acknowledged', 
            acknowledged_by = ?,
            updated_at = ?
        WHERE id = ?
    """, (ack.acknowledged_by, datetime.now(), alarm_id))
    
    conn.commit()
    conn.close()
    
    return {"message": "Alarm acknowledged", "alarm_id": alarm_id}


@router.put("/{alarm_id}/resolve")
async def resolve_alarm(alarm_id: int, resolve: AlarmResolve):
    """
    解决告警
    
    标记告警已解决，状态变为 resolved
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # 检查告警是否存在
    cursor.execute("SELECT * FROM alarms WHERE id = ?", (alarm_id,))
    row = cursor.fetchone()
    
    if not row:
        conn.close()
        raise HTTPException(status_code=404, detail="Alarm not found")
    
    # 更新状态
    cursor.execute("""
        UPDATE alarms 
        SET status = 'resolved', 
            resolved_at = ?,
            updated_at = ?
        WHERE id = ?
    """, (datetime.now(), datetime.now(), alarm_id))
    
    conn.commit()
    conn.close()
    
    return {"message": "Alarm resolved", "alarm_id": alarm_id}


@router.get("/statistics/overview")
async def get_alarm_statistics():
    """
    获取告警统计概览
    
    返回各级别告警数量、趋势等
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # 统计各级别告警数量
    cursor.execute("""
        SELECT level, COUNT(*) as count
        FROM alarms
        WHERE status = 'active'
        GROUP BY level
    """)
    level_stats = {row['level']: row['count'] for row in cursor.fetchall()}
    
    # 统计各状态告警数量
    cursor.execute("""
        SELECT status, COUNT(*) as count
        FROM alarms
        GROUP BY status
    """)
    status_stats = {row['status']: row['count'] for row in cursor.fetchall()}
    
    # 统计最近24小时新增告警
    cursor.execute("""
        SELECT COUNT(*) as count
        FROM alarms
        WHERE created_at >= datetime('now', '-24 hours')
    """)
    new_alarms_24h = cursor.fetchone()['count']
    
    conn.close()
    
    return {
        "level_distribution": level_stats,
        "status_distribution": status_stats,
        "new_alarms_24h": new_alarms_24h,
        "alarm_levels": ALARM_LEVELS,
        "alarm_types": ALARM_TYPES
    }


@router.delete("/{alarm_id}")
async def delete_alarm(alarm_id: int):
    """删除告警"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM alarms WHERE id = ?", (alarm_id,))
    row = cursor.fetchone()
    
    if not row:
        conn.close()
        raise HTTPException(status_code=404, detail="Alarm not found")
    
    cursor.execute("DELETE FROM alarms WHERE id = ?", (alarm_id,))
    conn.commit()
    conn.close()
    
    return {"message": "Alarm deleted", "alarm_id": alarm_id}
