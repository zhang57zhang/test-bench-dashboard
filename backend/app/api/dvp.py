"""
DVP Dashboard API Routes
DVP进度看板 API 路由（本地实现）
"""

from fastapi import APIRouter, Query
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime, timedelta
import random
import json
from pathlib import Path

router = APIRouter(prefix="/dvp", tags=["DVP Dashboard"])

# ============ 数据模型 ============

class Project(BaseModel):
    """项目"""
    project_id: str
    name: str
    total_experiments: int
    total_devices: int
    progress: float
    param_checked: bool
    is_interrupted: bool
    created_at: str
    updated_at: str

class Experiment(BaseModel):
    """实验组"""
    project_id: str
    experiment_id: str
    name: str
    total_devices: int
    completed_devices: int
    progress: float
    param_checked: bool
    is_interrupted: bool

class Device(BaseModel):
    """设备"""
    project_id: str
    experiment_id: str
    device_id: str
    name: str
    status: str  # running, idle, error, completed
    progress: float

class ProjectStatistics(BaseModel):
    """项目统计"""
    total_projects: int
    running_projects: int
    completed_projects: int
    interrupted_projects: int
    average_progress: float

# ============ 数据存储（内存） ============

# 项目数据存储
PROJECTS_DATA: List[dict] = []
DATA_FILE = Path(__file__).parent.parent.parent / "data" / "dvp_projects.json"

def generate_mock_projects():
    """生成模拟项目数据"""
    if PROJECTS_DATA:
        return PROJECTS_DATA
    
    projects = []
    for i in range(10):
        project_id = f"proj_{i:04d}"
        total_experiments = random.randint(10, 30)
        total_devices = total_experiments * random.randint(5, 15)
        progress = random.uniform(0, 100)
        
        project = {
            "project_id": project_id,
            "name": f"控制器项目 {i+1}",
            "total_experiments": total_experiments,
            "total_devices": total_devices,
            "progress": round(progress, 1),
            "param_checked": random.choice([True, False]),
            "is_interrupted": random.random() < 0.1,  # 10%概率中断
            "created_at": (datetime.now() - timedelta(days=random.randint(1, 30))).isoformat(),
            "updated_at": datetime.now().isoformat()
        }
        projects.append(project)
    
    PROJECTS_DATA.extend(projects)
    return projects

def save_projects_to_file():
    """保存项目数据到文件"""
    DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(PROJECTS_DATA, f, ensure_ascii=False, indent=2)

def load_projects_from_file():
    """从文件加载项目数据"""
    global PROJECTS_DATA
    if DATA_FILE.exists():
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            PROJECTS_DATA = json.load(f)
    return PROJECTS_DATA

# ============ API 端点 ============

@router.get("/projects", response_model=List[Project])
async def get_projects(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000)
):
    """获取所有项目列表"""
    if not PROJECTS_DATA:
        generate_mock_projects()
    
    return PROJECTS_DATA[skip:skip+limit]

@router.get("/projects/{project_id}", response_model=Project)
async def get_project(project_id: str):
    """获取单个项目详情"""
    if not PROJECTS_DATA:
        generate_mock_projects()
    
    for project in PROJECTS_DATA:
        if project["project_id"] == project_id:
            return project
    
    return {"error": "Project not found"}

@router.get("/statistics", response_model=ProjectStatistics)
async def get_statistics():
    """获取统计信息"""
    if not PROJECTS_DATA:
        generate_mock_projects()
    
    total = len(PROJECTS_DATA)
    running = sum(1 for p in PROJECTS_DATA if p["progress"] < 100 and not p["is_interrupted"])
    completed = sum(1 for p in PROJECTS_DATA if p["progress"] >= 100)
    interrupted = sum(1 for p in PROJECTS_DATA if p["is_interrupted"])
    avg_progress = sum(p["progress"] for p in PROJECTS_DATA) / total if total > 0 else 0
    
    return ProjectStatistics(
        total_projects=total,
        running_projects=running,
        completed_projects=completed,
        interrupted_projects=interrupted,
        average_progress=round(avg_progress, 1)
    )

@router.get("/projects/{project_id}/experiments", response_model=List[Experiment])
async def get_experiments(project_id: str):
    """获取项目的实验组列表"""
    experiments = []
    for i in range(random.randint(5, 15)):
        exp_id = f"{project_id}_exp_{i:04d}"
        total_devices = random.randint(5, 20)
        completed = random.randint(0, total_devices)
        
        experiments.append(Experiment(
            project_id=project_id,
            experiment_id=exp_id,
            name=f"实验组 {i+1}",
            total_devices=total_devices,
            completed_devices=completed,
            progress=round(completed / total_devices * 100, 1),
            param_checked=random.choice([True, False]),
            is_interrupted=random.random() < 0.05
        ))
    
    return experiments

@router.get("/projects/{project_id}/experiments/{experiment_id}/devices", response_model=List[Device])
async def get_devices(project_id: str, experiment_id: str):
    """获取实验组的设备列表"""
    devices = []
    for i in range(random.randint(5, 20)):
        devices.append(Device(
            project_id=project_id,
            experiment_id=experiment_id,
            device_id=f"{experiment_id}_dev_{i:04d}",
            name=f"设备 {i+1}",
            status=random.choice(["running", "idle", "completed", "error"]),
            progress=random.uniform(0, 100)
        ))
    
    return devices

@router.post("/projects/generate")
async def regenerate_projects():
    """重新生成模拟数据"""
    global PROJECTS_DATA
    PROJECTS_DATA.clear()
    generate_mock_projects()
    save_projects_to_file()
    return {"message": "数据已重新生成", "count": len(PROJECTS_DATA)}

@router.post("/projects/save")
async def save_projects():
    """保存当前数据到文件"""
    save_projects_to_file()
    return {"message": "数据已保存", "file": str(DATA_FILE)}
