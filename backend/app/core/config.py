"""
系统配置文件
使用 Pydantic Settings 进行配置管理
"""

from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field


class Settings(BaseSettings):
    """
    应用配置类
    从环境变量或 .env 文件中读取配置
    """
    
    # ==================== 数据库配置 ====================
    DATABASE_URL: str = Field(default="mysql+pymysql://wxy:Wxy123..@106.15.36.199:3306/pet_management")
    
    # ==================== JWT认证配置 ====================
    SECRET_KEY: str = Field(default="your-secret-key-here-change-in-production-min-32-chars")
    ALGORITHM: str = Field(default="HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(default=30)
    
    # ==================== CORS跨域配置 ====================
    CORS_ORIGINS: str = Field(default="http://localhost:5173,http://localhost:3000")
    
    # ==================== 环境配置 ====================
    ENVIRONMENT: str = Field(default="development")
    DEBUG: bool = Field(default=True)
    
    # ==================== 应用配置 ====================
    APP_NAME: str = Field(default="宠物管理系统")
    APP_VERSION: str = Field(default="1.0.0")
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore"
    )


# 创建全局配置实例
settings = Settings()
