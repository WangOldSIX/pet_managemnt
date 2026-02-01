"""
FastAPI应用主入口
Pet Management System Backend
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.core.exceptions import (
    business_exception_handler,
    sqlalchemy_exception_handler,
    general_exception_handler,
    BusinessException
)
from sqlalchemy.exc import SQLAlchemyError
from app.api import api_router

# 创建FastAPI应用实例
app = FastAPI(
    title=settings.APP_NAME,
    description="基于FastAPI + MySQL的宠物管理系统后端，数据库课程设计项目",
    version=settings.APP_VERSION,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)

# ==================== 配置CORS中间件 ====================
# 允许跨域请求，支持前后端分离
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ==================== 注册全局异常处理器 ====================
# 业务异常处理器
app.add_exception_handler(BusinessException, business_exception_handler)

# 数据库异常处理器
app.add_exception_handler(SQLAlchemyError, sqlalchemy_exception_handler)

# 通用异常处理器
app.add_exception_handler(Exception, general_exception_handler)

# ==================== 注册API路由 ====================
app.include_router(api_router, prefix="/api")


# ==================== 根路径 ====================
@app.get("/", tags=["根路径"])
async def root():
    """
    根路径接口
    
    Returns:
        dict: 欢迎信息
    """
    return {
        "message": "欢迎使用宠物管理系统API",
        "version": settings.APP_VERSION,
        "docs": "/docs",
        "redoc": "/redoc"
    }


# ==================== 健康检查 ====================
@app.get("/health", tags=["系统"])
async def health_check():
    """
    健康检查接口
    
    用于服务健康检查，确认服务是否正常运行
    
    Returns:
        dict: 健康状态
    """
    return {
        "status": "ok",
        "environment": settings.ENVIRONMENT,
        "app_name": settings.APP_NAME,
        "version": settings.APP_VERSION
    }


# ==================== 应用启动事件 ====================
@app.on_event("startup")
async def startup_event():
    """
    应用启动时执行的操作
    可以用于初始化资源、建立连接等
    """
    print(f"""
    ╔════════════════════════════════════════╗
    ║  🐾 {settings.APP_NAME} v{settings.APP_VERSION} ║
    ║  ═══════════════════════════════════  ║
    ║  📍 环境: {settings.ENVIRONMENT}                     ║
    ║  📚 文档: http://localhost:8000/docs    ║
    ║  🏥 健康检查: http://localhost:8000/health  ║
    ╚════════════════════════════════════════╝
    """)


# ==================== 应用关闭事件 ====================
@app.on_event("shutdown")
async def shutdown_event():
    """
    应用关闭时执行的操作
    可以用于释放资源、关闭连接等
    """
    print("应用正在关闭...")


if __name__ == "__main__":
    import uvicorn
    
    # 使用uvicorn启动应用
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG,
        log_level="info"
    )
