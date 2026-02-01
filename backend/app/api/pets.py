"""
宠物档案API模块
Pet Management API
"""

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.core.database import get_db
from app.core.deps import get_current_active_user, require_staff
from app.core.response import ApiResponse, PageResponse
from app.schemas import PetCreate, PetUpdate, PetResponse
from app.service import PetService
from app.db.models import User

router = APIRouter()


@router.get("", response_model=PageResponse[List[PetResponse]], summary="获取宠物列表")
async def get_pets(
    owner_id: Optional[int] = Query(None, description="主人ID"),
    page: int = Query(1, ge=1, description="页码"),
    size: int = Query(10, ge=1, le=100, description="每页数量"),
    name: str = Query(None, description="宠物名称筛选"),
    species: str = Query(None, description="物种筛选"),
    gender: str = Query(None, description="性别筛选"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    获取宠物列表（分页）
    
    宠物主人只能查看自己的宠物
    """
    if current_user.role.value == "owner":
        owner_id = current_user.id
    
    pets, total = PetService.get_pet_list(db, owner_id, page, size, name, species, gender)
    
    return PageResponse[List[PetResponse]](
        data={
            "items": [PetResponse.model_validate(p) for p in pets],
            "total": total,
            "page": page,
            "size": size
        }
    )


@router.get("/{pet_id}", response_model=ApiResponse[PetResponse], summary="获取宠物详情")
async def get_pet(
    pet_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """获取宠物详情"""
    pet = PetService.get_pet_detail(db, pet_id)
    
    if current_user.role.value == "owner" and pet.owner_id != current_user.id:
        return ApiResponse[PetResponse](code=403, msg="无权限查看此宠物信息", data=None)
    
    return ApiResponse[PetResponse](data=PetResponse.model_validate(pet))


@router.post("", response_model=ApiResponse[PetResponse], summary="创建宠物")
async def create_pet(
    pet: PetCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """创建宠物档案"""
    owner_id = current_user.id if current_user.role.value == "owner" else pet.owner_id
    new_pet = PetService.create_pet_info(db, pet, owner_id)
    return ApiResponse[PetResponse](data=PetResponse.model_validate(new_pet))


@router.put("/{pet_id}", response_model=ApiResponse[PetResponse], summary="更新宠物")
async def update_pet(
    pet_id: int,
    pet_update: PetUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """更新宠物信息"""
    pet = PetService.get_pet_detail(db, pet_id)
    
    if current_user.role.value == "owner" and pet.owner_id != current_user.id:
        return ApiResponse[PetResponse](code=403, msg="无权限修改此宠物信息", data=None)
    
    updated_pet = PetService.update_pet_info(db, pet_id, pet_update)
    return ApiResponse[PetResponse](data=PetResponse.model_validate(updated_pet))


@router.delete("/{pet_id}", response_model=ApiResponse[bool], summary="删除宠物")
async def delete_pet(
    pet_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """删除宠物"""
    pet = PetService.get_pet_detail(db, pet_id)
    
    if current_user.role.value == "owner" and pet.owner_id != current_user.id:
        return ApiResponse[PetResponse](code=403, msg="无权限删除此宠物", data=None)
    
    PetService.remove_pet(db, pet_id)
    return ApiResponse[bool](data=True)
