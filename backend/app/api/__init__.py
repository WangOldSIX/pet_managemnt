"""
API路由模块
API Router Module
"""

from fastapi import APIRouter
from app.api import auth, users, pets, services, orders, boardings, health_records, dashboard

# 创建API路由器
api_router = APIRouter()

# 注册各模块路由
# 认证模块
api_router.include_router(auth.router, prefix="/auth", tags=["认证"])

# 用户管理模块
api_router.include_router(users.router, prefix="/users", tags=["用户管理"])

# 宠物档案模块
api_router.include_router(pets.router, prefix="/pets", tags=["宠物档案"])

# 服务管理模块
api_router.include_router(services.router, prefix="/services", tags=["服务管理"])

# 订单管理模块
api_router.include_router(orders.router, prefix="/orders", tags=["订单管理"])

# 寄养管理模块
api_router.include_router(boardings.router, prefix="/boardings", tags=["寄养管理"])

# 健康记录模块
api_router.include_router(health_records.router, prefix="/health-records", tags=["健康记录"])

# 仪表盘模块
api_router.include_router(dashboard.router, prefix="/dashboard", tags=["仪表盘"])
