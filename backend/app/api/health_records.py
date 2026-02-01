"""
健康记录API模块
Health Record API
"""

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.core.database import get_db
from app.core.deps import get_current_active_user, require_staff
from app.core.response import ApiResponse, PageResponse
from app.schemas import HealthRecordCreate, HealthRecordUpdate, HealthRecordResponse
from app.service import HealthRecordService
from app.db.models import User

router = APIRouter()


@router.get("", response_model=PageResponse[List[HealthRecordResponse]], summary="获取健康记录列表")
async def get_health_records(
    pet_id: Optional[int] = Query(None, description="宠物ID"),
    vet_id: Optional[int] = Query(None, description="兽医ID"),
    record_type: Optional[str] = Query(None, description="记录类型"),
    page: int = Query(1, ge=1, description="页码"),
    size: int = Query(10, ge=1, le=100, description="每页数量"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """获取健康记录列表（分页）"""
    records, total = HealthRecordService.get_health_record_list(db, pet_id, vet_id, record_type, page, size)
    
    return PageResponse[List[HealthRecordResponse]](
        data={
            "items": [HealthRecordResponse.model_validate(r) for r in records],
            "total": total,
            "page": page,
            "size": size
        }
    )


@router.get("/{record_id}", response_model=ApiResponse[HealthRecordResponse], summary="获取健康记录详情")
async def get_health_record(
    record_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """获取健康记录详情"""
    record = HealthRecordService.get_health_record_detail(db, record_id)
    return ApiResponse[HealthRecordResponse](data=HealthRecordResponse.model_validate(record))


@router.post("", response_model=ApiResponse[HealthRecordResponse], summary="创建健康记录")
async def create_health_record(
    record: HealthRecordCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_staff)
):
    """创建健康记录 - 需要员工或管理员权限"""
    new_record = HealthRecordService.create_health_record_info(db, record)
    return ApiResponse[HealthRecordResponse](data=HealthRecordResponse.model_validate(new_record))


@router.put("/{record_id}", response_model=ApiResponse[HealthRecordResponse], summary="更新健康记录")
async def update_health_record(
    record_id: int,
    record_update: HealthRecordUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_staff)
):
    """更新健康记录 - 需要员工或管理员权限"""
    updated_record = HealthRecordService.update_health_record_info(db, record_id, record_update)
    return ApiResponse[HealthRecordResponse](data=HealthRecordResponse.model_validate(updated_record))


@router.delete("/{record_id}", response_model=ApiResponse[bool], summary="删除健康记录")
async def delete_health_record(
    record_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_staff)
):
    """删除健康记录 - 需要员工或管理员权限"""
    HealthRecordService.remove_health_record(db, record_id)
    return ApiResponse[bool](data=True)
