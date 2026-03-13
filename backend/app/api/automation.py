"""
Automation Dashboard API Routes
自动化测试看板 API 路由
"""

from fastapi import APIRouter, Query
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime, timedelta
import random

router = APIRouter(prefix="/automation", tags=["Automation Dashboard"])

# ============ 数据模型 ============

class AutomationStats(BaseModel):
    """自动化测试统计"""
    total_test_cases: int
    total_execution_time_hours: float
    total_manual_effort_saved_hours: float
    total_projects: int
    pass_rate: float

class ProjectAutomationStats(BaseModel):
    """项目自动化统计"""
    project_name: str
    test_cases: int
    execution_time_hours: float
    pass_rate: float
    failed_count: int

class DailyStats(BaseModel):
    """每日统计"""
    date: str
    test_cases: int
    execution_time_hours: float
    pass_rate: float
    failed_count: int

class AutomationMetrics(BaseModel):
    """完整指标"""
    overview: AutomationStats
    by_project: List[ProjectAutomationStats]
    by_period: List[DailyStats]

# ============ 模拟数据生成 ============

def generate_mock_data():
    """生成模拟数据"""
    projects = [
        {"name": "新能源控制器V1.0", "cases": random.randint(500, 1000)},
        {"name": "电池管理系统V2.0", "cases": random.randint(300, 600)},
        {"name": "电机控制器V3.0", "cases": random.randint(400, 800)},
        {"name": "充电系统V1.5", "cases": random.randint(200, 400)},
        {"name": "热管理系统V2.0", "cases": random.randint(150, 300)},
    ]

    by_project = []
    total_cases = 0
    total_time = 0
    total_failed = 0

    for proj in projects:
        cases = proj["cases"]
        time_hours = cases * random.uniform(0.005, 0.015)  # 每个用例平均执行时间
        pass_rate = random.uniform(0.85, 0.98)
        failed = int(cases * (1 - pass_rate))

        by_project.append(ProjectAutomationStats(
            project_name=proj["name"],
            test_cases=cases,
            execution_time_hours=round(time_hours, 2),
            pass_rate=round(pass_rate * 100, 1),
            failed_count=failed
        ))

        total_cases += cases
        total_time += time_hours
        total_failed += failed

    # 按天生成最近30天的数据
    by_period = []
    for i in range(30):
        date = (datetime.now() - timedelta(days=29-i)).strftime("%Y-%m-%d")
        cases = random.randint(50, 200)
        time_hours = cases * random.uniform(0.005, 0.015)
        pass_rate = random.uniform(0.85, 0.98)

        by_period.append(DailyStats(
            date=date,
            test_cases=cases,
            execution_time_hours=round(time_hours, 2),
            pass_rate=round(pass_rate * 100, 1),
            failed_count=int(cases * (1 - pass_rate))
        ))

    # 计算总览
    overview = AutomationStats(
        total_test_cases=total_cases,
        total_execution_time_hours=round(total_time, 2),
        total_manual_effort_saved_hours=round(total_time * 8, 2),  # 假设自动化是手动的8倍效率
        total_projects=len(projects),
        pass_rate=round((total_cases - total_failed) / total_cases * 100, 1)
    )

    return AutomationMetrics(
        overview=overview,
        by_project=by_project,
        by_period=by_period
    )

# ============ API 端点 ============

@router.get("/metrics", response_model=AutomationMetrics)
async def get_automation_metrics(
    period: str = Query("day", description="统计周期: day, week, month, year"),
    project: Optional[str] = Query(None, description="项目名称筛选")
):
    """
    获取自动化测试指标

    - **period**: 统计周期 (day/week/month/year)
    - **project**: 可选的项目名称筛选
    """
    data = generate_mock_data()

    # 根据period调整返回的数据
    if period == "week":
        # 返回最近7天
        data.by_period = data.by_period[-7:]
    elif period == "month":
        # 返回最近30天
        pass  # 已经是30天
    elif period == "year":
        # 返回最近365天（这里简化为30天）
        pass

    # 根据project筛选
    if project:
        data.by_project = [p for p in data.by_project if project.lower() in p.project_name.lower()]

    return data

@router.get("/overview", response_model=AutomationStats)
async def get_automation_overview():
    """获取自动化测试总览数据"""
    data = generate_mock_data()
    return data.overview

@router.get("/by-project", response_model=List[ProjectAutomationStats])
async def get_stats_by_project():
    """按项目获取统计"""
    data = generate_mock_data()
    return data.by_project

@router.get("/by-period", response_model=List[DailyStats])
async def get_stats_by_period(
    period: str = Query("day", description="统计周期: day, week, month, year")
):
    """
    按时间周期获取统计

    - **period**: 统计周期 (day/week/month/year)
    """
    data = generate_mock_data()

    if period == "week":
        return data.by_period[-7:]
    elif period == "month":
        return data.by_period
    elif period == "year":
        # 简化处理，返回30天数据
        return data.by_period
    else:
        return data.by_period
