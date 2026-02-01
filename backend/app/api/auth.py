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
from app.schemas import UserLogin, UserResponse, TokenResponse
from app.service import UserService

# 创建路由器
router = APIRouter()


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
