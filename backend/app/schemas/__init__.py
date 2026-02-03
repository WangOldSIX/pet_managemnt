"""
数据模型模块
Pydantic Schemas for API request/response validation
"""

from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel, EmailStr, Field, ConfigDict
from enum import Enum


# ==================== 枚举类型定义 ====================

class UserRole(str, Enum):
    """用户角色"""
    admin = "admin"  # 管理员
    owner = "owner"  # 宠物主人
    staff = "staff"  # 员工


class OrderStatus(str, Enum):
    """订单状态"""
    pending = "pending"           # 待确认
    confirmed = "confirmed"       # 已确认
    in_progress = "in_progress"   # 进行中
    completed = "completed"       # 已完成
    cancelled = "cancelled"       # 已取消


class BoardingStatus(str, Enum):
    """寄养状态"""
    scheduled = "scheduled"       # 已预约
    in_progress = "in_progress"   # 进行中
    completed = "completed"       # 已完成
    cancelled = "cancelled"       # 已取消


class Gender(str, Enum):
    """性别"""
    male = "male"     # 公
    female = "female" # 母


class HealthRecordType(str, Enum):
    """健康记录类型"""
    checkup = "checkup"           # 检查
    treatment = "treatment"       # 治疗
    vaccination = "vaccination"   # 疫苗
    surgery = "surgery"           # 手术


# ==================== 通用模型基类 ====================

class BaseSchema(BaseModel):
    """基础Schema配置"""
    model_config = ConfigDict(from_attributes=True, use_enum_values=True)


class TimestampMixin(BaseModel):
    """时间戳混入类，为模型添加创建时间和更新时间字段"""
    created_at: datetime = Field(..., description="创建时间")
    updated_at: datetime = Field(..., description="更新时间")


# ==================== 用户相关 Schema ====================

class UserBase(BaseSchema):
    """用户基础信息"""
    username: str = Field(..., min_length=3, max_length=50, description="用户名")
    email: Optional[EmailStr] = Field(None, description="邮箱")
    phone: Optional[str] = Field(None, max_length=20, description="手机号")
    real_name: Optional[str] = Field(None, max_length=50, description="真实姓名")


class UserCreate(UserBase):
    """创建用户请求模型"""
    password: str = Field(..., min_length=6, max_length=100, description="密码")
    role: UserRole = Field(default=UserRole.owner, description="角色")


class UserUpdate(BaseSchema):
    """更新用户请求模型"""
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    real_name: Optional[str] = None
    avatar: Optional[str] = None
    is_active: Optional[bool] = None


class UserResponse(UserBase, TimestampMixin):
    """用户响应模型"""
    id: int = Field(..., description="用户ID")
    role: UserRole = Field(..., description="角色")
    avatar: Optional[str] = Field(None, description="头像URL")
    is_active: bool = Field(..., description="是否启用")


class UserLogin(BaseSchema):
    """用户登录请求模型"""
    username: str = Field(..., description="用户名")
    password: str = Field(..., description="密码")


class UserRegister(BaseSchema):
    """用户注册请求模型"""
    username: str = Field(..., min_length=3, max_length=50, description="用户名")
    password: str = Field(..., min_length=6, max_length=100, description="密码")
    confirm_password: str = Field(..., min_length=6, max_length=100, description="确认密码")
    email: Optional[EmailStr] = Field(None, description="邮箱")
    phone: Optional[str] = Field(None, max_length=20, description="手机号")
    real_name: Optional[str] = Field(None, max_length=50, description="真实姓名")


class TokenResponse(BaseSchema):
    """登录响应模型，包含Token和用户信息"""
    access_token: str = Field(..., description="访问令牌")
    token_type: str = Field(default="bearer", description="令牌类型")
    user: UserResponse = Field(..., description="用户信息")


# ==================== 宠物相关 Schema ====================

class PetBase(BaseSchema):
    """宠物基础信息"""
    name: str = Field(..., min_length=1, max_length=50, description="宠物名称")
    species: str = Field(..., max_length=50, description="物种")
    breed: Optional[str] = Field(None, max_length=50, description="品种")
    gender: Gender = Field(..., description="性别")
    birth_date: Optional[datetime] = Field(None, description="出生日期")
    weight: Optional[float] = Field(None, ge=0, description="体重(kg)")
    color: Optional[str] = Field(None, max_length=50, description="毛色")
    health_status: Optional[str] = Field(None, description="健康状况")
    special_notes: Optional[str] = Field(None, description="特殊备注")


class PetCreate(PetBase):
    """创建宠物请求模型"""
    pass


class PetUpdate(BaseSchema):
    """更新宠物请求模型"""
    name: Optional[str] = None
    species: Optional[str] = None
    breed: Optional[str] = None
    gender: Optional[Gender] = None
    birth_date: Optional[datetime] = None
    weight: Optional[float] = None
    color: Optional[str] = None
    health_status: Optional[str] = None
    special_notes: Optional[str] = None
    avatar: Optional[str] = None


class PetResponse(PetBase, TimestampMixin):
    """宠物响应模型"""
    id: int = Field(..., description="宠物ID")
    owner_id: int = Field(..., description="主人ID")
    avatar: Optional[str] = Field(None, description="宠物照片URL")


# ==================== 服务相关 Schema ====================

class ServiceBase(BaseSchema):
    """服务基础信息"""
    name: str = Field(..., min_length=1, max_length=100, description="服务名称")
    description: Optional[str] = Field(None, description="服务描述")
    category: str = Field(..., max_length=50, description="服务类别")
    price: float = Field(..., gt=0, description="服务价格")
    duration: Optional[int] = Field(None, ge=0, description="服务时长(分钟)")


class ServiceCreate(ServiceBase):
    """创建服务请求模型"""
    pass


class ServiceUpdate(BaseSchema):
    """更新服务请求模型"""
    name: Optional[str] = None
    description: Optional[str] = None
    category: Optional[str] = None
    price: Optional[float] = None
    duration: Optional[int] = None
    image: Optional[str] = None
    is_available: Optional[bool] = None


class ServiceResponse(ServiceBase, TimestampMixin):
    """服务响应模型"""
    id: int = Field(..., description="服务ID")
    image: Optional[str] = Field(None, description="服务图片URL")
    is_available: bool = Field(..., description="是否上架")


# ==================== 订单相关 Schema ====================

class OrderBase(BaseSchema):
    """订单基础信息"""
    pet_id: int = Field(..., description="宠物ID")
    service_id: int = Field(..., description="服务ID")
    appointment_time: Optional[datetime] = Field(None, description="预约时间")
    notes: Optional[str] = Field(None, description="备注")


class OrderCreate(OrderBase):
    """创建订单请求模型"""
    pass


class OrderUpdate(BaseSchema):
    """更新订单请求模型"""
    staff_id: Optional[int] = None
    status: Optional[OrderStatus] = None
    appointment_time: Optional[datetime] = None
    notes: Optional[str] = None


class OrderResponse(OrderBase, TimestampMixin):
    """订单响应模型"""
    id: int = Field(..., description="订单ID")
    order_no: str = Field(..., description="订单号")
    user_id: int = Field(..., description="用户ID")
    staff_id: Optional[int] = Field(None, description="服务员工ID")
    status: OrderStatus = Field(..., description="订单状态")
    total_amount: float = Field(..., description="订单总额")


# ==================== 寄养相关 Schema ====================

class BoardingBase(BaseSchema):
    """寄养基础信息"""
    pet_id: int = Field(..., description="宠物ID")
    staff_id: int = Field(..., description="饲养员ID")
    start_date: datetime = Field(..., description="寄养开始时间")
    end_date: datetime = Field(..., description="寄养结束时间")


class BoardingCreate(BoardingBase):
    """创建寄养请求模型"""
    pass


class BoardingUpdate(BaseSchema):
    """更新寄养请求模型"""
    status: Optional[BoardingStatus] = None
    daily_notes: Optional[str] = None
    food_type: Optional[str] = None
    feeding_schedule: Optional[str] = None


class BoardingResponse(BoardingBase, TimestampMixin):
    """寄养响应模型"""
    id: int = Field(..., description="寄养ID")
    order_id: int = Field(..., description="订单ID")
    status: BoardingStatus = Field(..., description="寄养状态")


# ==================== 健康记录相关 Schema ====================

class HealthRecordBase(BaseSchema):
    """健康记录基础信息"""
    pet_id: int = Field(..., description="宠物ID")
    vet_id: int = Field(..., description="兽医ID")
    check_date: datetime = Field(..., description="检查日期")
    type: HealthRecordType = Field(..., description="记录类型")
    description: Optional[str] = Field(None, description="详细描述")
    diagnosis: Optional[str] = Field(None, description="诊断结果")
    prescription: Optional[str] = Field(None, description="处方信息")
    notes: Optional[str] = Field(None, description="备注")


class HealthRecordCreate(HealthRecordBase):
    """创建健康记录请求模型"""
    pass


class HealthRecordUpdate(BaseSchema):
    """更新健康记录请求模型"""
    check_date: Optional[datetime] = None
    type: Optional[HealthRecordType] = None
    description: Optional[str] = None
    diagnosis: Optional[str] = None
    prescription: Optional[str] = None
    notes: Optional[str] = None


class HealthRecordResponse(HealthRecordBase, TimestampMixin):
    """健康记录响应模型"""
    id: int = Field(..., description="健康记录ID")


# ==================== 仪表盘相关 Schema ====================

class DashboardStats(BaseSchema):
    """仪表盘统计数据模型"""
    total_users: int = Field(..., description="总用户数")
    total_pets: int = Field(..., description="总宠物数")
    total_orders: int = Field(..., description="总订单数")
    total_revenue: float = Field(..., description="总营收")
    active_orders: int = Field(..., description="进行中订单数")
