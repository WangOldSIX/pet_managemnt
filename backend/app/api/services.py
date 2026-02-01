"""
服务管理API模块
Service Management API
"""

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.core.database import get_db
from app.core.deps import get_current_active_user, require_staff
from app.core.response import ApiResponse, PageResponse
from app.schemas import ServiceCreate, ServiceUpdate, ServiceResponse
from app.service import ServiceService
from app.db.models import User

router = APIRouter()


@router.get("", response_model=PageResponse[List[ServiceResponse]], summary="获取服务列表")
async def get_services(
    category: Optional[str] = Query(None, description="服务类别"),
    is_available: Optional[bool] = Query(None, description="是否上架"),
    page: int = Query(1, ge=1, description="页码"),
    size: int = Query(10, ge=1, le=100, description="每页数量"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """获取服务列表（分页）"""
    services, total = ServiceService.get_service_list(db, page, size, category, is_available)
    
    return PageResponse[List[ServiceResponse]](
        data={
            "items": [ServiceResponse.model_validate(s) for s in services],
            "total": total,
            "page": page,
            "size": size
        }
    )


@router.get("/{service_id}", response_model=ApiResponse[ServiceResponse], summary="获取服务详情")
async def get_service(
    service_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """获取服务详情"""
    service = ServiceService.get_service_detail(db, service_id)
    return ApiResponse[ServiceResponse](data=ServiceResponse.model_validate(service))


@router.post("", response_model=ApiResponse[ServiceResponse], summary="创建服务")
async def create_service(
    service: ServiceCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_staff)
):
    """创建新服务 - 需要员工或管理员权限"""
    new_service = ServiceService.create_service_info(db, service)
    return ApiResponse[ServiceResponse](data=ServiceResponse.model_validate(new_service))


@router.put("/{service_id}", response_model=ApiResponse[ServiceResponse], summary="更新服务")
async def update_service(
    service_id: int,
    service_update: ServiceUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_staff)
):
    """更新服务信息 - 需要员工或管理员权限"""
    updated_service = ServiceService.update_service_info(db, service_id, service_update)
    return ApiResponse[ServiceResponse](data=ServiceResponse.model_validate(updated_service))


@router.delete("/{service_id}", response_model=ApiResponse[bool], summary="删除服务")
async def delete_service(
    service_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_staff)
):
    """删除服务 - 需要员工或管理员权限"""
    ServiceService.remove_service(db, service_id)
    return ApiResponse[bool](data=True)
