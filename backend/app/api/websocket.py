"""
WebSocket API
实时通信端点
"""

from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from typing import List
import asyncio
import json
from datetime import datetime

router = APIRouter(tags=["websocket"])


class ConnectionManager:
    """WebSocket 连接管理器"""
    
    def __init__(self):
        self.active_connections: List[WebSocket] = []
    
    async def connect(self, websocket: WebSocket):
        """接受新连接"""
        await websocket.accept()
        self.active_connections.append(websocket)
        print(f"[WebSocket] New connection. Total: {len(self.active_connections)}")
    
    def disconnect(self, websocket: WebSocket):
        """断开连接"""
        self.active_connections.remove(websocket)
        print(f"[WebSocket] Disconnected. Total: {len(self.active_connections)}")
    
    async def send_personal_message(self, message: str, websocket: WebSocket):
        """发送个人消息"""
        try:
            await websocket.send_text(message)
        except Exception as e:
            print(f"[WebSocket] Error sending message: {e}")
    
    async def broadcast(self, message: str):
        """广播消息给所有连接"""
        for connection in self.active_connections:
            try:
                await connection.send_text(message)
            except Exception as e:
                print(f"[WebSocket] Error broadcasting: {e}")
                # 移除断开的连接
                if connection in self.active_connections:
                    self.active_connections.remove(connection)


# 全局连接管理器
manager = ConnectionManager()


@router.websocket("/ws/devices")
async def websocket_devices(websocket: WebSocket):
    """
    设备状态实时推送
    
    功能：
    - 实时推送设备状态更新
    - 支持多客户端连接
    - 自动重连机制
    """
    await manager.connect(websocket)
    
    try:
        # 发送欢迎消息
        await websocket.send_json({
            "type": "connected",
            "message": "WebSocket connected successfully",
            "timestamp": datetime.now().isoformat()
        })
        
        # 保持连接
        while True:
            # 接收客户端消息（心跳/订阅）
            data = await websocket.receive_text()
            
            try:
                message = json.loads(data)
                
                # 处理心跳
                if message.get("type") == "ping":
                    await websocket.send_json({
                        "type": "pong",
                        "timestamp": datetime.now().isoformat()
                    })
                
                # 处理订阅请求
                elif message.get("type") == "subscribe":
                    topic = message.get("topic")
                    await websocket.send_json({
                        "type": "subscribed",
                        "topic": topic,
                        "timestamp": datetime.now().isoformat()
                    })
            
            except json.JSONDecodeError:
                # 非JSON消息，忽略
                pass
            
            except Exception as e:
                print(f"[WebSocket] Error processing message: {e}")
    
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        print("[WebSocket] Client disconnected")
    
    except Exception as e:
        manager.disconnect(websocket)
        print(f"[WebSocket] Connection error: {e}")


@router.websocket("/ws/alarms")
async def websocket_alarms(websocket: WebSocket):
    """
    告警实时推送
    
    功能：
    - 实时推送新告警
    - 告警状态更新通知
    """
    await manager.connect(websocket)
    
    try:
        await websocket.send_json({
            "type": "connected",
            "message": "Alarm WebSocket connected",
            "timestamp": datetime.now().isoformat()
        })
        
        while True:
            data = await websocket.receive_text()
            # 处理心跳等
            await asyncio.sleep(1)
    
    except WebSocketDisconnect:
        manager.disconnect(websocket)


@router.websocket("/ws/metrics")
async def websocket_metrics(websocket: WebSocket):
    """
    性能指标实时推送
    
    功能：
    - 实时推送性能指标
    - 定期更新统计数据
    """
    await manager.connect(websocket)
    
    try:
        await websocket.send_json({
            "type": "connected",
            "message": "Metrics WebSocket connected",
            "timestamp": datetime.now().isoformat()
        })
        
        while True:
            data = await websocket.receive_text()
            # 处理心跳等
            await asyncio.sleep(1)
    
    except WebSocketDisconnect:
        manager.disconnect(websocket)


# 辅助函数：推送设备更新
async def push_device_update(device_data: dict):
    """推送设备状态更新"""
    message = json.dumps({
        "type": "device_update",
        "data": device_data,
        "timestamp": datetime.now().isoformat()
    })
    await manager.broadcast(message)


# 辅助函数：推送新告警
async def push_new_alarm(alarm_data: dict):
    """推送新告警"""
    message = json.dumps({
        "type": "new_alarm",
        "data": alarm_data,
        "timestamp": datetime.now().isoformat()
    })
    await manager.broadcast(message)


# 辅助函数：推送性能指标更新
async def push_metrics_update(metrics_data: dict):
    """推送性能指标更新"""
    message = json.dumps({
        "type": "metrics_update",
        "data": metrics_data,
        "timestamp": datetime.now().isoformat()
    })
    await manager.broadcast(message)
