"""
数据库连接配置
配置 SQLAlchemy 数据库连接和会话管理
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

# ==================== 创建数据库引擎 ====================
# pool_pre_ping=True: 连接池ping检查，避免连接断开问题
# pool_recycle=3600: 连接回收时间，3600秒后回收连接
# echo=settings.DEBUG: 开发环境下输出SQL语句，便于调试
engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True,
    pool_recycle=3600,
    echo=settings.DEBUG
)

# ==================== 创建会话工厂 ====================
# autocommit=False: 不自动提交事务
# autoflush=False: 不自动刷新session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# ==================== 创建模型基类 ====================
# 所有 SQLAlchemy 模型都继承自这个基类
Base = declarative_base()


# ==================== 数据库会话依赖注入 ====================
def get_db():
    """
    获取数据库会话的依赖注入函数
    用于 FastAPI 的依赖注入系统
    
    使用示例:
    ```python
    @app.get("/users")
    def get_users(db: Session = Depends(get_db)):
        return db.query(User).all()
    ```
    
    Returns:
        Session: SQLAlchemy 数据库会话
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
