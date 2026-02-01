"""
依赖注入模块
定义 FastAPI 的依赖注入函数，用于认证和权限控制
"""

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import decode_access_token
from app.db.models import User
from typing import Optional, List

# HTTP Bearer Token 认证方案
security = HTTPBearer()


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> User:
    """
    获取当前登录用户
    从 HTTP Bearer Token 中解析用户信息
    
    Args:
        credentials: HTTP Bearer Token 凭证
        db: 数据库会话
        
    Raises:
        HTTPException: 认证失败时抛出401异常
        
    Returns:
        User: 当前用户对象
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="无法验证凭据",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    # 获取Token
    token = credentials.credentials
    
    # 解码Token
    payload = decode_access_token(token)
    
    if payload is None:
        raise credentials_exception
    
    # 获取用户ID
    user_id: Optional[int] = payload.get("sub")
    if user_id is None:
        raise credentials_exception
    
    # 从数据库查询用户
    user = db.query(User).filter(User.id == user_id, User.is_deleted == False).first()
    if user is None:
        raise credentials_exception
    
    return user


async def get_current_active_user(current_user: User = Depends(get_current_user)) -> User:
    """
    获取当前活跃用户
    检查用户是否被禁用
    
    Args:
        current_user: 当前用户对象
        
    Raises:
        HTTPException: 用户被禁用时抛出400异常
        
    Returns:
        User: 当前活跃用户对象
    """
    if not current_user.is_active:
        raise HTTPException(
            status_code=400,
            detail="用户未激活"
        )
    return current_user


class RoleChecker:
    """
    角色检查器类
    用于检查用户是否拥有指定角色权限
    
    使用示例:
    ```python
    # 只允许管理员访问
    admin_required = RoleChecker(["admin"])
    
    @app.get("/admin/dashboard")
    def admin_dashboard(user: User = Depends(admin_required)):
        return {"message": "Welcome admin"}
    ```
    """
    
    def __init__(self, allowed_roles: list):
        """
        初始化角色检查器
        
        Args:
            allowed_roles: 允许的角色列表，如 ["admin", "staff"]
        """
        self.allowed_roles = allowed_roles
    
    def __call__(self, current_user: User = Depends(get_current_active_user)) -> User:
        """
        检查用户角色是否在允许的角色列表中
        
        Args:
            current_user: 当前用户对象
            
        Raises:
            HTTPException: 角色不匹配时抛出403异常
            
        Returns:
            User: 通过权限检查的用户对象
        """
        if current_user.role.value not in self.allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"权限不足，需要角色：{', '.join(self.allowed_roles)}"
            )
        return current_user


# ==================== 预定义的角色检查依赖 ====================
# 管理员权限
require_admin = RoleChecker(["admin"])

# 员工权限（包含管理员）
require_staff = RoleChecker(["admin", "staff"])

# 宠物主人权限（包含员工和管理员）
require_owner = RoleChecker(["admin", "staff", "owner"])
