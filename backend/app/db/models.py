"""
数据库模型定义
使用 SQLAlchemy ORM 定义所有数据库表模型
对应数据库中的6张表
"""

from sqlalchemy import Column, BigInteger, String, Boolean, DateTime, Text, Enum, ForeignKey, Date, Numeric, Integer
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
from app.core.database import Base


# ==================== 枚举类型定义 ====================

class UserRole(str, enum.Enum):
    """用户角色枚举"""
    admin = "admin"      # 管理员
    owner = "owner"      # 宠物主人
    staff = "staff"      # 员工


class OrderStatus(str, enum.Enum):
    """订单状态枚举"""
    pending = "pending"           # 待确认
    confirmed = "confirmed"       # 已确认
    in_progress = "in_progress"   # 进行中
    completed = "completed"       # 已完成
    cancelled = "cancelled"       # 已取消


class BoardingStatus(str, enum.Enum):
    """寄养状态枚举"""
    scheduled = "scheduled"       # 已预约
    in_progress = "in_progress"   # 进行中
    completed = "completed"       # 已完成
    cancelled = "cancelled"       # 已取消


class Gender(str, enum.Enum):
    """性别枚举"""
    male = "male"     # 公
    female = "female" # 母


class HealthRecordType(str, enum.Enum):
    """健康记录类型枚举"""
    checkup = "checkup"           # 检查
    treatment = "treatment"       # 治疗
    vaccination = "vaccination"   # 疫苗
    surgery = "surgery"           # 手术


# ==================== 数据库模型定义 ====================

class User(Base):
    """
    用户表模型
    对应数据库表：users
    存储系统用户信息，包含管理员、宠物主人、员工三种角色
    """
    __tablename__ = "users"
    
    # 字段定义
    id = Column(BigInteger, primary_key=True, autoincrement=True, comment="用户ID")
    username = Column(String(50), unique=True, nullable=False, comment="用户名")
    password = Column(String(255), nullable=False, comment="密码")
    email = Column(String(100), nullable=True, comment="邮箱")
    phone = Column(String(20), nullable=True, comment="手机号")
    real_name = Column(String(50), nullable=True, comment="真实姓名")
    role = Column(Enum(UserRole), nullable=False, default=UserRole.owner, comment="角色")
    avatar = Column(String(255), nullable=True, comment="头像URL")
    is_active = Column(Boolean, default=True, nullable=False, comment="是否启用")
    is_deleted = Column(Boolean, default=False, nullable=False, comment="是否删除")
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False, comment="创建时间")
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False, comment="更新时间")
    
    # 关系定义
    # 一对多关系：一个用户可以拥有多只宠物
    pets = relationship("Pet", back_populates="owner", cascade="all, delete-orphan")
    
    # 一对多关系：一个用户可以有多个订单（作为订单发起者）
    orders = relationship("Order", back_populates="user", foreign_keys="Order.user_id", cascade="all, delete-orphan")
    
    # 一对多关系：一个员工可以服务多个订单
    staff_orders = relationship("Order", back_populates="staff", foreign_keys="Order.staff_id")
    
    # 一对多关系：一个员工可以负责多个寄养
    boardings = relationship("Boarding", back_populates="staff", cascade="all, delete-orphan")
    
    # 一对多关系：一个兽医可以有多条健康记录
    health_records = relationship("HealthRecord", back_populates="vet", cascade="all, delete-orphan")
    
    def __repr__(self):
        """对象的字符串表示"""
        return f"<User(id={self.id}, username='{self.username}', role='{self.role}')>"


class Pet(Base):
    """
    宠物档案表模型
    对应数据库表：pets
    存储宠物的基本信息
    """
    __tablename__ = "pets"
    
    # 字段定义
    id = Column(BigInteger, primary_key=True, autoincrement=True, comment="宠物ID")
    owner_id = Column(BigInteger, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, comment="主人ID")
    name = Column(String(50), nullable=False, comment="宠物名称")
    species = Column(String(50), nullable=False, comment="物种")
    breed = Column(String(50), nullable=True, comment="品种")
    gender = Column(Enum(Gender), nullable=False, comment="性别")
    birth_date = Column(Date, nullable=True, comment="出生日期")
    weight = Column(Numeric(5, 2), nullable=True, comment="体重")
    color = Column(String(50), nullable=True, comment="毛色")
    health_status = Column(Text, nullable=True, comment="健康状况")
    special_notes = Column(Text, nullable=True, comment="特殊备注")
    avatar = Column(String(255), nullable=True, comment="照片URL")
    is_deleted = Column(Boolean, default=False, nullable=False, comment="是否删除")
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False, comment="创建时间")
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False, comment="更新时间")
    
    # 关系定义
    # 多对一关系：多只宠物属于一个用户
    owner = relationship("User", back_populates="pets")
    
    # 一对多关系：一只宠物可以有多个订单
    orders = relationship("Order", back_populates="pet", cascade="all, delete-orphan")
    
    # 一对多关系：一只宠物可以有多条寄养记录
    boardings = relationship("Boarding", back_populates="pet", cascade="all, delete-orphan")
    
    # 一对多关系：一只宠物可以有多条健康记录
    health_records = relationship("HealthRecord", back_populates="pet", cascade="all, delete-orphan")
    
    def __repr__(self):
        """对象的字符串表示"""
        return f"<Pet(id={self.id}, name='{self.name}', species='{self.species}')>"


class Service(Base):
    """
    宠物服务表模型
    对应数据库表：services
    存储系统提供的各项服务信息
    """
    __tablename__ = "services"
    
    # 字段定义
    id = Column(BigInteger, primary_key=True, autoincrement=True, comment="服务ID")
    name = Column(String(100), nullable=False, comment="服务名称")
    description = Column(Text, nullable=True, comment="服务描述")
    category = Column(String(50), nullable=False, comment="服务类别")
    price = Column(Numeric(10, 2), nullable=False, comment="服务价格")
    duration = Column(Integer, nullable=True, comment="服务时长(分钟)")
    image = Column(String(255), nullable=True, comment="服务图片URL")
    is_available = Column(Boolean, default=True, nullable=False, comment="是否上架")
    is_deleted = Column(Boolean, default=False, nullable=False, comment="是否删除")
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False, comment="创建时间")
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False, comment="更新时间")
    
    # 关系定义
    # 一对多关系：一个服务可以出现在多个订单中
    orders = relationship("Order", back_populates="service")
    
    def __repr__(self):
        """对象的字符串表示"""
        return f"<Service(id={self.id}, name='{self.name}', category='{self.category}')>"


class Order(Base):
    """
    订单表模型
    对应数据库表：orders
    存储宠物服务的订单信息
    """
    __tablename__ = "orders"
    
    # 字段定义
    id = Column(BigInteger, primary_key=True, autoincrement=True, comment="订单ID")
    order_no = Column(String(50), unique=True, nullable=False, comment="订单号")
    user_id = Column(BigInteger, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, comment="用户ID")
    pet_id = Column(BigInteger, ForeignKey("pets.id", ondelete="CASCADE"), nullable=False, comment="宠物ID")
    service_id = Column(BigInteger, ForeignKey("services.id", ondelete="RESTRICT"), nullable=False, comment="服务ID")
    staff_id = Column(BigInteger, ForeignKey("users.id", ondelete="SET NULL"), nullable=True, comment="服务员工ID")
    appointment_time = Column(DateTime, nullable=True, comment="预约时间")
    status = Column(Enum(OrderStatus), default=OrderStatus.pending, nullable=False, comment="订单状态")
    total_amount = Column(Numeric(10, 2), nullable=False, comment="订单总额")
    notes = Column(Text, nullable=True, comment="备注")
    is_deleted = Column(Boolean, default=False, nullable=False, comment="是否删除")
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False, comment="创建时间")
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False, comment="更新时间")
    
    # 关系定义
    # 多对一关系：多个订单属于一个用户
    user = relationship("User", back_populates="orders", foreign_keys=[user_id])
    
    # 多对一关系：多个订单针对一只宠物
    pet = relationship("Pet", back_populates="orders")
    
    # 多对一关系：多个订单对应一个服务
    service = relationship("Service", back_populates="orders")
    
    # 多对一关系：多个订单由一个员工服务
    staff = relationship("User", back_populates="staff_orders", foreign_keys=[staff_id])
    
    # 一对多关系：一个订单可以对应一条寄养记录
    boardings = relationship("Boarding", back_populates="order", cascade="all, delete-orphan")
    
    def __repr__(self):
        """对象的字符串表示"""
        return f"<Order(id={self.id}, order_no='{self.order_no}', status='{self.status}')>"


class Boarding(Base):
    """
    寄养表模型
    对应数据库表：boardings
    存储宠物寄养的详细信息
    """
    __tablename__ = "boardings"
    
    # 字段定义
    id = Column(BigInteger, primary_key=True, autoincrement=True, comment="寄养ID")
    order_id = Column(BigInteger, ForeignKey("orders.id", ondelete="CASCADE"), nullable=False, comment="订单ID")
    pet_id = Column(BigInteger, ForeignKey("pets.id", ondelete="CASCADE"), nullable=False, comment="宠物ID")
    staff_id = Column(BigInteger, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, comment="饲养员ID")
    start_date = Column(DateTime, nullable=False, comment="寄养开始时间")
    end_date = Column(DateTime, nullable=False, comment="寄养结束时间")
    status = Column(Enum(BoardingStatus), default=BoardingStatus.scheduled, nullable=False, comment="寄养状态")
    daily_notes = Column(Text, nullable=True, comment="每日记录")
    food_type = Column(String(100), nullable=True, comment="食物类型")
    feeding_schedule = Column(String(100), nullable=True, comment="喂食计划")
    is_deleted = Column(Boolean, default=False, nullable=False, comment="是否删除")
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False, comment="创建时间")
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False, comment="更新时间")
    
    # 关系定义
    # 多对一关系：多条寄养记录属于一个订单
    order = relationship("Order", back_populates="boardings")
    
    # 多对一关系：多条寄养记录针对一只宠物
    pet = relationship("Pet", back_populates="boardings")
    
    # 多对一关系：多条寄养记录由一个员工负责
    staff = relationship("User", back_populates="boardings")
    
    def __repr__(self):
        """对象的字符串表示"""
        return f"<Boarding(id={self.id}, status='{self.status}', start_date='{self.start_date}')>"


class HealthRecord(Base):
    """
    健康记录表模型
    对应数据库表：health_records
    存储宠物健康检查和治疗记录
    """
    __tablename__ = "health_records"
    
    # 字段定义
    id = Column(BigInteger, primary_key=True, autoincrement=True, comment="健康记录ID")
    pet_id = Column(BigInteger, ForeignKey("pets.id", ondelete="CASCADE"), nullable=False, comment="宠物ID")
    vet_id = Column(BigInteger, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, comment="兽医ID")
    check_date = Column(DateTime, nullable=False, comment="检查日期")
    type = Column(Enum(HealthRecordType), nullable=False, comment="记录类型")
    description = Column(Text, nullable=True, comment="详细描述")
    diagnosis = Column(Text, nullable=True, comment="诊断结果")
    prescription = Column(Text, nullable=True, comment="处方信息")
    notes = Column(Text, nullable=True, comment="备注")
    is_deleted = Column(Boolean, default=False, nullable=False, comment="是否删除")
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False, comment="创建时间")
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False, comment="更新时间")
    
    # 关系定义
    # 多对一关系：多条健康记录针对一只宠物
    pet = relationship("Pet", back_populates="health_records")
    
    # 多对一关系：多条健康记录由一个兽医创建
    vet = relationship("User", back_populates="health_records")
    
    def __repr__(self):
        """对象的字符串表示"""
        return f"<HealthRecord(id={self.id}, type='{self.type}', check_date='{self.check_date}')>"
