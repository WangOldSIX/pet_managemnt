"""
认证API模块
Authentication API
处理用户登录和当前用户信息获取
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import create_access_token, timedelta
from app.core.deps import get_current_active_user
from app.core.response import ApiResponse
from app.schemas import UserLogin, UserRegister, UserResponse, TokenResponse
from app.service import UserService

# 创建路由器
router = APIRouter()


@router.post("/register", response_model=ApiResponse[UserResponse], summary="用户注册")
async def register(
    user_data: UserRegister,
    db: Session = Depends(get_db)
):
    """
    用户注册接口
    
    公开接口，允许新用户注册账号。默认注册为宠物主人角色。
    
    Args:
        user_data: 注册信息（用户名、密码、确认密码等）
        db: 数据库会话
        
    Returns:
        ApiResponse[UserResponse]: 注册成功的用户信息
        
    Raises:
        400: 两次密码不一致、用户名已存在
    """
    # 验证两次密码是否一致
    if user_data.password != user_data.confirm_password:
        return ApiResponse[UserResponse](code=400, msg="两次密码不一致", data=None)
    
    # 构造 UserCreate 对象（去掉确认密码字段）
    from app.schemas import UserCreate, UserRole
    user_create = UserCreate(
        username=user_data.username,
        password=user_data.password,
        email=user_data.email,
        phone=user_data.phone,
        real_name=user_data.real_name,
        role=UserRole.owner  # 默认注册为宠物主人
    )
    
    try:
        # 调用服务层进行注册
        new_user = UserService.register(db, user_create)
        return ApiResponse[UserResponse](
            data=UserResponse.model_validate(new_user)
        )
    except Exception as e:
        # 处理用户名已存在的异常
        error_msg = str(e)
        if "用户名已存在" in error_msg or "exists" in error_msg.lower():
            return ApiResponse[UserResponse](code=400, msg="用户名已存在", data=None)
        return ApiResponse[UserResponse](code=500, msg="注册失败，请稍后重试", data=None)


@router.post("/login", response_model=ApiResponse[TokenResponse], summary="用户登录")
async def login(
    credentials: UserLogin,
    db: Session = Depends(get_db)
):
    """
    用户登录接口
    
    验证用户名和密码，成功则返回访问令牌和用户信息
    
    Args:
        credentials: 登录凭证（用户名和密码）
        db: 数据库会话
        
    Returns:
        ApiResponse[TokenResponse]: 包含访问令牌和用户信息的响应
        
    Raises:
        401: 用户名或密码错误
        400: 账号已被禁用
    """
    # 调用服务层进行用户认证
    user = UserService.authenticate(db, credentials.username, credentials.password)
    if not user:
        return ApiResponse[TokenResponse](code=401, msg="用户名或密码错误", data=None)
    
    # 检查账号状态
    if not user.is_active:
        return ApiResponse[TokenResponse](code=400, msg="账号已被禁用", data=None)
    
    # 创建访问令牌
    access_token = create_access_token(data={"sub": str(user.id)})
    
    # 返回令牌和用户信息
    return ApiResponse[TokenResponse](
        data=TokenResponse(
            access_token=access_token,
            user=UserResponse.model_validate(user)
        )
    )


@router.get("/me", response_model=ApiResponse[UserResponse], summary="获取当前用户信息")
async def get_current_user_info(
    current_user = Depends(get_current_active_user)
):
    """
    获取当前登录用户的详细信息
    
    需要在请求头中携带有效的JWT Token
    
    Args:
        current_user: 当前登录用户（通过依赖注入自动获取）
        
    Returns:
        ApiResponse[UserResponse]: 当前用户信息
    """
    return ApiResponse[UserResponse](data=UserResponse.model_validate(current_user))
