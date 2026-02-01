"""
系统配置文件
使用 Pydantic Settings 进行配置管理
"""

from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    """
    应用配置类
    从环境变量或 .env 文件中读取配置
    """
    
    # ==================== 数据库配置 ====================
    DATABASE_URL: str = "mysql+pymysql://root:password@localhost:3306/pet_management"
    
    # ==================== JWT认证配置 ====================
    SECRET_KEY: str = "your-secret-key-here-change-in-production-min-32-chars"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # ==================== CORS跨域配置 ====================
    CORS_ORIGINS: List[str] = ["http://localhost:5173", "http://localhost:3000"]
    
    # ==================== 环境配置 ====================
    ENVIRONMENT: str = "development"
    DEBUG: bool = True
    
    # ==================== 应用配置 ====================
    APP_NAME: str = "宠物管理系统"
    APP_VERSION: str = "1.0.0"
    
    class Config:
        """配置加载器"""
        env_file = ".env"
        case_sensitive = True  # 区分大小写


# 创建全局配置实例
settings = Settings()
