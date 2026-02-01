"""
仪表盘API模块
Dashboard API
提供统计数据接口
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.deps import require_staff
from app.core.response import ApiResponse
from app.schemas import DashboardStats
from app.service import DashboardService

# 创建路由器
router = APIRouter()


@router.get("/stats", response_model=ApiResponse[DashboardStats], summary="获取统计数据")
async def get_stats(
    db: Session = Depends(get_db),
    current_user = Depends(require_staff)
):
    """
    获取仪表盘统计数据
    
    需要员工或管理员权限
    
    统计数据包括：
    - 总用户数
    - 总宠物数
    - 总订单数
    - 总营收（已完成订单）
    - 进行中订单数
    
    Args:
        db: 数据库会话
        current_user: 当前用户（需要员工或管理员权限）
        
    Returns:
        ApiResponse[DashboardStats]: 统计数据
    """
    stats = DashboardService.get_stats(db)
    return ApiResponse[DashboardStats](data=DashboardStats(**stats))
