"""
订单管理API模块
Order Management API
"""

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.core.database import get_db
from app.core.deps import get_current_active_user, require_staff
from app.core.response import ApiResponse, PageResponse
from app.schemas import OrderCreate, OrderUpdate, OrderResponse
from app.service import OrderService
from app.db.models import User

router = APIRouter()


@router.get("", response_model=PageResponse[List[OrderResponse]], summary="获取订单列表")
async def get_orders(
    user_id: Optional[int] = Query(None, description="用户ID"),
    pet_id: Optional[int] = Query(None, description="宠物ID"),
    status: Optional[str] = Query(None, description="订单状态"),
    page: int = Query(1, ge=1, description="页码"),
    size: int = Query(10, ge=1, le=100, description="每页数量"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    获取订单列表（分页）
    
    宠物主人只能查看自己的订单
    """
    if current_user.role.value == "owner":
        user_id = current_user.id
    
    orders, total = OrderService.get_order_list(db, user_id, pet_id, status, page, size)
    
    return PageResponse[List[OrderResponse]](
        data={
            "items": [OrderResponse.model_validate(o) for o in orders],
            "total": total,
            "page": page,
            "size": size
        }
    )


@router.get("/{order_id}", response_model=ApiResponse[OrderResponse], summary="获取订单详情")
async def get_order(
    order_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """获取订单详情"""
    order = OrderService.get_order_detail(db, order_id)
    
    if current_user.role.value == "owner" and order.user_id != current_user.id:
        return ApiResponse[OrderResponse](code=403, msg="无权限查看此订单", data=None)
    
    return ApiResponse[OrderResponse](data=OrderResponse.model_validate(order))


@router.post("", response_model=ApiResponse[OrderResponse], summary="创建订单")
async def create_order(
    order: OrderCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """创建新订单"""
    user_id = current_user.id if current_user.role.value == "owner" else order.user_id
    new_order = OrderService.create_order_info(db, order, user_id)
    return ApiResponse[OrderResponse](data=OrderResponse.model_validate(new_order))


@router.put("/{order_id}", response_model=ApiResponse[OrderResponse], summary="更新订单")
async def update_order(
    order_id: int,
    order_update: OrderUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """更新订单信息"""
    order = OrderService.get_order_detail(db, order_id)
    
    if current_user.role.value == "owner" and order.user_id != current_user.id:
        return ApiResponse[OrderResponse](code=403, msg="无权限修改此订单", data=None)
    
    updated_order = OrderService.update_order_info(db, order_id, order_update)
    return ApiResponse[OrderResponse](data=OrderResponse.model_validate(updated_order))


@router.delete("/{order_id}", response_model=ApiResponse[bool], summary="删除订单")
async def delete_order(
    order_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """删除订单"""
    order = OrderService.get_order_detail(db, order_id)
    
    if current_user.role.value == "owner" and order.user_id != current_user.id:
        return ApiResponse[OrderResponse](code=403, msg="无权限删除此订单", data=None)
    
    OrderService.remove_order(db, order_id)
    return ApiResponse[bool](data=True)
