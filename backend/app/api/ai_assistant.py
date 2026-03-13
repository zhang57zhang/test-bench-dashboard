"""
AI Assistant Dashboard API Routes
AI辅助看板 API 路由
"""

from fastapi import APIRouter, Query
from pydantic import BaseModel
from typing import List, Dict, Optional
from datetime import datetime, timedelta
import random

router = APIRouter(prefix="/ai-assistant", tags=["AI Assistant Dashboard"])

# ============ 数据模型 ============

class AIActivity(BaseModel):
    """AI活动类型"""
    name: str
    count: int
    percentage: float

class AIOverview(BaseModel):
    """AI辅助总览"""
    total_assistances: int
    total_manual_effort_saved_hours: float
    total_activities: int
    top_activity: str

class DailyAIStats(BaseModel):
    """每日AI统计"""
    date: str
    total_count: int
    by_activity: Dict[str, int]

class AIAssistantMetrics(BaseModel):
    """完整AI辅助指标"""
    overview: AIOverview
    by_activity: List[AIActivity]
    by_period: List[DailyAIStats]

# ============ 活动类型定义 ============

ACTIVITY_TYPES = [
    "需求分析",
    "测试策略",
    "测试设计",
    "用例编写",
    "用例审查",
    "脚本编写",
    "脚本调试",
    "脚本执行",
    "日志分析",
    "数据分析",
    "报告编写",
]

# ============ 模拟数据生成 ============

def generate_mock_ai_data():
    """生成模拟AI数据"""

    # 按活动类型统计
    by_activity = []
    total_count = 0
    activities_data = {}

    for activity in ACTIVITY_TYPES:
        count = random.randint(50, 500)
        activities_data[activity] = count
        total_count += count

    for activity, count in activities_data.items():
        by_activity.append(AIActivity(
            name=activity,
            count=count,
            percentage=round(count / total_count * 100, 1)
        ))

    # 按活动排序
    by_activity.sort(key=lambda x: x.count, reverse=True)

    # 按天生成最近30天的数据
    by_period = []
    for i in range(30):
        date = (datetime.now() - timedelta(days=29-i)).strftime("%Y-%m-%d")

        # 每天的活动分布
        daily_activities = {}
        daily_total = 0

        for activity in ACTIVITY_TYPES:
            count = random.randint(5, 50)
            daily_activities[activity] = count
            daily_total += count

        by_period.append(DailyAIStats(
            date=date,
            total_count=daily_total,
            by_activity=daily_activities
        ))

    # 计算总览
    overview = AIOverview(
        total_assistances=total_count,
        total_manual_effort_saved_hours=round(total_count * 0.5, 2),  # 假设每次辅助节省0.5小时
        total_activities=len(ACTIVITY_TYPES),
        top_activity=by_activity[0].name if by_activity else "无"
    )

    return AIAssistantMetrics(
        overview=overview,
        by_activity=by_activity,
        by_period=by_period
    )

# ============ API 端点 ============

@router.get("/metrics", response_model=AIAssistantMetrics)
async def get_ai_metrics(
    period: str = Query("day", description="统计周期: day, week, month, year")
):
    """
    获取AI辅助指标

    - **period**: 统计周期 (day/week/month/year)
    """
    data = generate_mock_ai_data()

    # 根据period调整返回的数据
    if period == "week":
        data.by_period = data.by_period[-7:]
    elif period == "month":
        pass  # 已经是30天
    elif period == "year":
        pass  # 简化处理

    return data

@router.get("/overview", response_model=AIOverview)
async def get_ai_overview():
    """获取AI辅助总览数据"""
    data = generate_mock_ai_data()
    return data.overview

@router.get("/by-activity", response_model=List[AIActivity])
async def get_stats_by_activity():
    """按活动类型获取统计"""
    data = generate_mock_ai_data()
    return data.by_activity

@router.get("/by-period", response_model=List[DailyAIStats])
async def get_stats_by_period(
    period: str = Query("day", description="统计周期: day, week, month, year")
):
    """
    按时间周期获取统计

    - **period**: 统计周期 (day/week/month/year)
    """
    data = generate_mock_ai_data()

    if period == "week":
        return data.by_period[-7:]
    elif period == "month":
        return data.by_period
    elif period == "year":
        return data.by_period
    else:
        return data.by_period
