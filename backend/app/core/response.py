"""
统一响应格式模块
定义API接口的统一响应格式
"""

from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union
from pydantic import BaseModel, Field
from pydantic.generics import GenericModel

# 泛型类型变量
T = TypeVar("T")


class ApiResponse(GenericModel, Generic[T]):
    """
    统一API响应格式
    所有接口都应使用此格式返回数据
    
    Attributes:
        code: 状态码，200表示成功
        msg: 响应消息，默认为"success"
        data: 响应数据，可以是任意类型
    """
    code: int = Field(default=200, description="状态码，200表示成功")
    msg: str = Field(default="success", description="响应消息")
    data: Optional[T] = Field(default=None, description="响应数据")


class PageInfo(BaseModel):
    """
    分页信息模型
    
    Attributes:
        total: 总记录数
        page: 当前页码
        size: 每页记录数
    """
    total: int = Field(..., description="总记录数")
    page: int = Field(..., description="当前页码")
    size: int = Field(..., description="每页记录数")


class PageResponse(GenericModel, Generic[T]):
    """
    分页响应格式
    用于返回分页数据
    
    Attributes:
        code: 状态码
        msg: 响应消息
        data: 包含items和分页信息的字典
    """
    code: int = Field(default=200, description="状态码")
    msg: str = Field(default="success", description="响应消息")
    data: Dict[str, Any] = Field(
        default_factory=dict,
        description="包含items列表和分页信息"
    )
