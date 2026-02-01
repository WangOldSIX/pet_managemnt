"""
寄养管理API模块
Boarding Management API
"""

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.core.database import get_db
from app.core.deps import get_current_active_user, require_staff
from app.core.response import ApiResponse, PageResponse
from app.schemas import BoardingCreate, BoardingUpdate, BoardingResponse
from app.service import BoardingService
from app.db.models import User

router = APIRouter()


@router.get("", response_model=PageResponse[List[BoardingResponse]], summary="获取寄养列表")
async def get_boardings(
    staff_id: Optional[int] = Query(None, description="饲养员ID"),
    pet_id: Optional[int] = Query(None, description="宠物ID"),
    status: Optional[str] = Query(None, description="寄养状态"),
    page: int = Query(1, ge=1, description="页码"),
    size: int = Query(10, ge=1, le=100, description="每页数量"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """获取寄养记录列表（分页）"""
    boardings, total = BoardingService.get_boarding_list(db, staff_id, pet_id, status, page, size)
    
    return PageResponse[List[BoardingResponse]](
        data={
            "items": [BoardingResponse.model_validate(b) for b in boardings],
            "total": total,
            "page": page,
            "size": size
        }
    )


@router.get("/{boarding_id}", response_model=ApiResponse[BoardingResponse], summary="获取寄养详情")
async def get_boarding(
    boarding_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """获取寄养详情"""
    boarding = BoardingService.get_boarding_detail(db, boarding_id)
    return ApiResponse[BoardingResponse](data=BoardingResponse.model_validate(boarding))


@router.post("", response_model=ApiResponse[BoardingResponse], summary="创建寄养记录")
async def create_boarding(
    boarding: BoardingCreate,
    order_id: int = Query(..., description="订单ID"),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_staff)
):
    """创建寄养记录 - 需要员工或管理员权限"""
    new_boarding = BoardingService.create_boarding_info(db, boarding, order_id)
    return ApiResponse[BoardingResponse](data=BoardingResponse.model_validate(new_boarding))


@router.put("/{boarding_id}", response_model=ApiResponse[BoardingResponse], summary="更新寄养记录")
async def update_boarding(
    boarding_id: int,
    boarding_update: BoardingUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_staff)
):
    """更新寄养信息 - 需要员工或管理员权限"""
    updated_boarding = BoardingService.update_boarding_info(db, boarding_id, boarding_update)
    return ApiResponse[BoardingResponse](data=BoardingResponse.model_validate(updated_boarding))


@router.delete("/{boarding_id}", response_model=ApiResponse[bool], summary="删除寄养记录")
async def delete_boarding(
    boarding_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_staff)
):
    """删除寄养记录 - 需要员工或管理员权限"""
    BoardingService.remove_boarding(db, boarding_id)
    return ApiResponse[bool](data=True)
