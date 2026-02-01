"""
安全模块
处理密码加密和 JWT Token 认证
"""

from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from app.core.config import settings

# ==================== 密码加密上下文 ====================
# 使用 bcrypt 算法进行密码加密
# bcrypt 是一种安全的密码哈希算法，具有加盐机制
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    验证密码
    
    Args:
        plain_password: 明文密码
        hashed_password: 哈希后的密码
        
    Returns:
        bool: 密码是否匹配
    """
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """
    加密密码
    
    Args:
        password: 明文密码
        
    Returns:
        str: 哈希后的密码
    """
    return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    创建访问令牌 (JWT Token)
    
    Args:
        data: 要编码的数据字典，通常包含用户ID等信息
        expires_delta: 过期时间增量，None则使用默认过期时间
        
    Returns:
        str: JWT Token 字符串
    """
    # 复制数据，避免修改原始数据
    to_encode = data.copy()
    
    # 设置过期时间
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    # 添加过期时间到payload
    to_encode.update({"exp": expire})
    
    # 编码生成JWT Token
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt


def decode_access_token(token: str) -> Optional[dict]:
    """
    解码访问令牌 (JWT Token)
    
    Args:
        token: JWT Token 字符串
        
    Returns:
        dict: 解码后的payload，失败返回None
    """
    try:
        # 解码Token
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        return payload
    except JWTError:
        # Token无效或过期
        return None
