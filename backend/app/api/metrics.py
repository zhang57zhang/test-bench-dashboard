"""
Metrics API
性能指标 API
"""

from fastapi import APIRouter, Query
from typing import Optional
from datetime import datetime, timedelta
import sqlite3
from app.core.database import get_db_connection

router = APIRouter(prefix="/api/v1/metrics", tags=["metrics"])


@router.get("/overview")
async def get_overview_metrics():
    """
    获取综合性能指标
    
    包含设备利用率、测试通过率等核心指标
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # 设备总数
    cursor.execute("SELECT COUNT(*) as count FROM devices")
    total_devices = cursor.fetchone()['count']
    
    # 在线设备数
    cursor.execute("SELECT COUNT(*) as count FROM devices WHERE status = 'online'")
    online_devices = cursor.fetchone()['count']
    
    # 运行中设备数
    cursor.execute("SELECT COUNT(*) as count FROM devices WHERE status = 'running'")
    running_devices = cursor.fetchone()['count']
    
    # 维护中设备数
    cursor.execute("SELECT COUNT(*) as count FROM devices WHERE status = 'maintenance'")
    maintenance_devices = cursor.fetchone()['count']
    
    # 故障设备数
    cursor.execute("SELECT COUNT(*) as count FROM devices WHERE status = 'offline'")
    offline_devices = cursor.fetchone()['count']
    
    # 设备利用率（简化计算）
    device_utilization = (running_devices / total_devices * 100) if total_devices > 0 else 0
    
    # 设备可用率
    device_availability = ((online_devices + running_devices) / total_devices * 100) if total_devices > 0 else 0
    
    # 自动化测试统计
    cursor.execute("SELECT COUNT(*) as count FROM automation_tests")
    total_tests = cursor.fetchone()['count']
    
    cursor.execute("SELECT COUNT(*) as count FROM automation_tests WHERE status = 'passed'")
    passed_tests = cursor.fetchone()['count']
    
    test_pass_rate = (passed_tests / total_tests * 100) if total_tests > 0 else 0
    
    # DVP 统计
    cursor.execute("SELECT COUNT(*) as count FROM dvp_projects")
    total_projects = cursor.fetchone()['count']
    
    cursor.execute("SELECT COUNT(*) as count FROM dvp_projects WHERE status = 'in_progress'")
    active_projects = cursor.fetchone()['count']
    
    # AI 辅助统计
    cursor.execute("SELECT SUM(assist_count) as total FROM ai_assistant_activities")
    result = cursor.fetchone()
    total_ai_assists = result['total'] if result['total'] else 0
    
    # 告警统计
    cursor.execute("SELECT COUNT(*) as count FROM alarms WHERE status = 'active'")
    active_alarms = cursor.fetchone()['count']
    
    cursor.execute("SELECT COUNT(*) as count FROM alarms WHERE level = 'P0' AND status = 'active'")
    p0_alarms = cursor.fetchone()['count']
    
    conn.close()
    
    return {
        "devices": {
            "total": total_devices,
            "online": online_devices,
            "running": running_devices,
            "maintenance": maintenance_devices,
            "offline": offline_devices,
            "utilization": round(device_utilization, 2),
            "availability": round(device_availability, 2)
        },
        "tests": {
            "total": total_tests,
            "passed": passed_tests,
            "pass_rate": round(test_pass_rate, 2)
        },
        "projects": {
            "total": total_projects,
            "active": active_projects
        },
        "ai_assistant": {
            "total_assists": total_ai_assists
        },
        "alarms": {
            "active": active_alarms,
            "p0": p0_alarms
        },
        "timestamp": datetime.now().isoformat()
    }


@router.get("/devices")
async def get_device_metrics(
    device_id: Optional[int] = None,
    days: int = Query(7, ge=1, le=90)
):
    """
    获取设备性能指标
    
    参数：
    - device_id: 设备ID（可选，不传则返回所有设备）
    - days: 统计天数（默认7天）
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    
    if device_id:
        # 单个设备指标
        cursor.execute("SELECT * FROM devices WHERE id = ?", (device_id,))
        device = cursor.fetchone()
        
        if not device:
            conn.close()
            return {"error": "Device not found"}
        
        # 计算设备利用率（基于历史数据）
        # 这里简化处理，实际应该从历史记录表计算
        utilization = 85.0 if device['status'] == 'running' else 0.0
        
        # MTBF（平均故障间隔时间）- 简化计算
        cursor.execute("""
            SELECT COUNT(*) as count FROM alarms 
            WHERE device_id = ? AND type = 'hardware_failure' 
            AND created_at >= datetime('now', '-{} days')
        """.format(days))
        failure_count = cursor.fetchone()['count']
        
        mtbf = (days * 24) / failure_count if failure_count > 0 else 999
        
        # MTTR（平均修复时间）- 简化计算
        cursor.execute("""
            SELECT AVG(julianday(resolved_at) - julianday(created_at)) * 24 as avg_hours
            FROM alarms 
            WHERE device_id = ? AND resolved_at IS NOT NULL
            AND created_at >= datetime('now', '-{} days')
        """.format(days))
        result = cursor.fetchone()
        mttr = result['avg_hours'] if result['avg_hours'] else 0
        
        conn.close()
        
        return {
            "device_id": device_id,
            "device_name": device['name'],
            "utilization": utilization,
            "mtbf": round(mtbf, 2),  # 小时
            "mttr": round(mttr, 2),  # 小时
            "availability": round(100 - (mttr / (mtbf + mttr) * 100), 2) if mtbf < 999 else 99.9,
            "period_days": days
        }
    else:
        # 所有设备指标汇总
        cursor.execute("SELECT * FROM devices")
        devices = cursor.fetchall()
        
        metrics_list = []
        for device in devices:
            # 简化计算
            utilization = 85.0 if device['status'] == 'running' else 0.0
            
            metrics_list.append({
                "device_id": device['id'],
                "device_name": device['name'],
                "status": device['status'],
                "utilization": utilization
            })
        
        conn.close()
        
        return {
            "devices": metrics_list,
            "total": len(metrics_list),
            "period_days": days
        }


@router.get("/tests")
async def get_test_metrics(
    days: int = Query(7, ge=1, le=90)
):
    """
    获取测试性能指标
    
    参数：
    - days: 统计天数（默认7天）
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # 总测试数
    cursor.execute("""
        SELECT COUNT(*) as count FROM automation_tests
        WHERE executed_at >= datetime('now', '-{} days')
    """.format(days))
    total_tests = cursor.fetchone()['count']
    
    # 通过的测试数
    cursor.execute("""
        SELECT COUNT(*) as count FROM automation_tests
        WHERE status = 'passed'
        AND executed_at >= datetime('now', '-{} days')
    """.format(days))
    passed_tests = cursor.fetchone()['count']
    
    # 失败的测试数
    cursor.execute("""
        SELECT COUNT(*) as count FROM automation_tests
        WHERE status = 'failed'
        AND executed_at >= datetime('now', '-{} days')
    """.format(days))
    failed_tests = cursor.fetchone()['count']
    
    # 平均执行时长
    cursor.execute("""
        SELECT AVG(duration) as avg_duration FROM automation_tests
        WHERE executed_at >= datetime('now', '-{} days')
    """.format(days))
    result = cursor.fetchone()
    avg_duration = result['avg_duration'] if result['avg_duration'] else 0
    
    # 节省人力（人天）
    cursor.execute("""
        SELECT SUM(saved_man_hours) as total FROM automation_tests
        WHERE executed_at >= datetime('now', '-{} days')
    """.format(days))
    result = cursor.fetchone()
    saved_man_hours = result['total'] if result['total'] else 0
    saved_man_days = saved_man_hours / 8  # 8小时/天
    
    # 测试通过率
    pass_rate = (passed_tests / total_tests * 100) if total_tests > 0 else 0
    
    conn.close()
    
    return {
        "total_tests": total_tests,
        "passed_tests": passed_tests,
        "failed_tests": failed_tests,
        "pass_rate": round(pass_rate, 2),
        "avg_duration": round(avg_duration, 2),
        "saved_man_hours": saved_man_hours,
        "saved_man_days": round(saved_man_days, 2),
        "period_days": days,
        "timestamp": datetime.now().isoformat()
    }


@router.get("/trend/devices")
async def get_device_trend(days: int = Query(30, ge=7, le=90)):
    """
    获取设备利用率趋势
    
    返回最近N天的设备利用率趋势数据
    """
    # 这里返回模拟数据，实际应该从历史记录表查询
    trend_data = []
    for i in range(days):
        date = datetime.now() - timedelta(days=i)
        trend_data.append({
            "date": date.strftime("%Y-%m-%d"),
            "utilization": 80 + (i % 10),  # 模拟数据
            "availability": 95 + (i % 5)
        })
    
    return {
        "trend": trend_data,
        "period_days": days
    }


@router.get("/trend/tests")
async def get_test_trend(days: int = Query(30, ge=7, le=90)):
    """
    获取测试通过率趋势
    
    返回最近N天的测试通过率趋势数据
    """
    # 这里返回模拟数据，实际应该从历史记录表查询
    trend_data = []
    for i in range(days):
        date = datetime.now() - timedelta(days=i)
        trend_data.append({
            "date": date.strftime("%Y-%m-%d"),
            "pass_rate": 95 + (i % 5),  # 模拟数据
            "total_tests": 100 + (i * 2)
        })
    
    return {
        "trend": trend_data,
        "period_days": days
    }
