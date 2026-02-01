"""
异常处理模块
定义自定义异常和全局异常处理器
"""

from fastapi import Request
from fastapi.responses import JSONResponse
from sqlalchemy.exc import SQLAlchemyError
import logging

# 配置日志
logger = logging.getLogger(__name__)


# ==================== 自定义业务异常类 ====================

class BusinessException(Exception):
    """
    业务异常基类
    所有的业务异常都应该继承这个类
    """
    def __init__(self, code: int, msg: str, data=None):
        """
        初始化业务异常
        
        Args:
            code: 错误码
            msg: 错误信息
            data: 返回的数据（可选）
        """
        self.code = code
        self.msg = msg
        self.data = data


class NotFoundError(BusinessException):
    """资源未找到异常 (404)"""
    def __init__(self, msg: str = "资源不存在"):
        super().__init__(code=404, msg=msg)


class ValidationError(BusinessException):
    """参数验证异常 (400)"""
    def __init__(self, msg: str = "参数验证失败"):
        super().__init__(code=400, msg=msg)


class UnauthorizedError(BusinessException):
    """未授权异常 (401)"""
    def __init__(self, msg: str = "未授权"):
        super().__init__(code=401, msg=msg)


class ForbiddenError(BusinessException):
    """禁止访问异常 (403)"""
    def __init__(self, msg: str = "禁止访问"):
        super().__init__(code=403, msg=msg)


class ConflictError(BusinessException):
    """资源冲突异常 (409)"""
    def __init__(self, msg: str = "资源冲突"):
        super().__init__(code=409, msg=msg)


# ==================== 全局异常处理器 ====================

async def business_exception_handler(request: Request, exc: BusinessException):
    """
    业务异常处理器
    处理所有的业务异常，返回统一的JSON格式
    
    Args:
        request: 请求对象
        exc: 业务异常对象
        
    Returns:
        JSONResponse: 统一格式的错误响应
    """
    return JSONResponse(
        status_code=200,
        content={
            "code": exc.code,
            "msg": exc.msg,
            "data": exc.data
        }
    )


async def sqlalchemy_exception_handler(request: Request, exc: SQLAlchemyError):
    """
    数据库异常处理器
    处理所有的SQLAlchemy数据库操作异常
    
    Args:
        request: 请求对象
        exc: SQLAlchemy异常对象
        
    Returns:
        JSONResponse: 统一格式的错误响应
    """
    logger.error(f"数据库错误: {str(exc)}")
    return JSONResponse(
        status_code=200,
        content={
            "code": 500,
            "msg": "数据库操作失败",
            "data": None
        }
    )


async def general_exception_handler(request: Request, exc: Exception):
    """
    通用异常处理器
    处理所有未被其他处理器捕获的异常
    
    Args:
        request: 请求对象
        exc: 异常对象
        
    Returns:
        JSONResponse: 统一格式的错误响应
    """
    logger.error(f"系统错误: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=200,
        content={
            "code": 500,
            "msg": "服务器内部错误",
            "data": None
        }
    )
