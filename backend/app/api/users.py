"""
用户管理API模块
User Management API
"""

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.core.deps import get_current_active_user, require_admin
from app.core.response import ApiResponse, PageResponse
from app.schemas import UserCreate, UserUpdate, UserResponse
from app.service import UserService
from app.db.models import User

router = APIRouter()


@router.get("", response_model=PageResponse[List[UserResponse]], summary="获取用户列表")
async def get_users(
    page: int = Query(1, ge=1, description="页码"),
    size: int = Query(10, ge=1, le=100, description="每页数量"),
    username: str = Query(None, description="用户名筛选"),
    role: str = Query(None, description="角色筛选"),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    """
    获取用户列表（分页）
    
    需要管理员权限
    """
    users, total = UserService.get_user_list(db, page, size, username, role)
    
    return PageResponse[List[UserResponse]](
        data={
            "items": [UserResponse.model_validate(u) for u in users],
            "total": total,
            "page": page,
            "size": size
        }
    )


@router.get("/{user_id}", response_model=ApiResponse[UserResponse], summary="获取用户详情")
async def get_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """获取用户详情"""
    if current_user.role.value != "admin" and current_user.id != user_id:
        return ApiResponse[UserResponse](code=403, msg="无权限查看其他用户信息", data=None)
    
    user = UserService.get_user_detail(db, user_id)
    return ApiResponse[UserResponse](data=UserResponse.model_validate(user))


@router.post("", response_model=ApiResponse[UserResponse], summary="创建用户")
async def create_user(
    user: UserCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    """创建新用户 - 需要管理员权限"""
    new_user = UserService.register(db, user)
    return ApiResponse[UserResponse](data=UserResponse.model_validate(new_user))


@router.put("/{user_id}", response_model=ApiResponse[UserResponse], summary="更新用户")
async def update_user(
    user_id: int,
    user_update: UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """更新用户信息"""
    if current_user.role.value != "admin" and current_user.id != user_id:
        return ApiResponse[UserResponse](code=403, msg="无权限修改其他用户信息", data=None)
    
    user = UserService.update_user_info(db, user_id, user_update)
    return ApiResponse[UserResponse](data=UserResponse.model_validate(user))


@router.delete("/{user_id}", response_model=ApiResponse[bool], summary="删除用户")
async def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    """删除用户 - 需要管理员权限"""
    UserService.remove_user(db, user_id)
    return ApiResponse[bool](data=True)
