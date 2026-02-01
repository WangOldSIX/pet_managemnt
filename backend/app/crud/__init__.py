"""
数据访问层 (CRUD)
Data Access Layer
提供所有数据库操作的CRUD函数
"""

from typing import List, Optional, Tuple
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, func, desc, asc
from app.db.models import User, Pet, Service, Order, Boarding, HealthRecord
from app.schemas import (
    UserCreate, UserUpdate,
    PetCreate, PetUpdate,
    ServiceCreate, ServiceUpdate,
    OrderCreate, OrderUpdate,
    BoardingCreate, BoardingUpdate,
    HealthRecordCreate, HealthRecordUpdate
)
from datetime import datetime
import random
import string


# ==================== 通用工具函数 ====================

def generate_order_no() -> str:
    """
    生成订单号
    格式：ORD + 时间戳(年月日时分秒) + 4位随机数
    
    Returns:
        str: 订单号，如 ORD20250201143012001
    """
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    random_str = ''.join(random.choices(string.digits, k=4))
    return f"ORD{timestamp}{random_str}"


# ==================== 用户 CRUD 操作 ====================

def get_user(db: Session, user_id: int) -> Optional[User]:
    """
    根据ID获取用户
    
    Args:
        db: 数据库会话
        user_id: 用户ID
        
    Returns:
        User: 用户对象，不存在返回None
    """
    return db.query(User).filter(User.id == user_id, User.is_deleted == False).first()


def get_user_by_username(db: Session, username: str) -> Optional[User]:
    """
    根据用户名获取用户
    
    Args:
        db: 数据库会话
        username: 用户名
        
    Returns:
        User: 用户对象，不存在返回None
    """
    return db.query(User).filter(User.username == username, User.is_deleted == False).first()


def get_users(
    db: Session,
    skip: int = 0,
    limit: int = 10,
    username: Optional[str] = None,
    role: Optional[str] = None
) -> Tuple[List[User], int]:
    """
    获取用户列表（分页+筛选）
    
    Args:
        db: 数据库会话
        skip: 跳过记录数（分页偏移量）
        limit: 返回记录数（每页数量）
        username: 用户名筛选（模糊查询）
        role: 角色筛选
        
    Returns:
        Tuple[List[User], int]: 用户列表和总记录数
    """
    # 构建查询
    query = db.query(User).filter(User.is_deleted == False)
    
    # 用户名模糊查询
    if username:
        query = query.filter(User.username.like(f"%{username}%"))
    
    # 角色筛选
    if role:
        query = query.filter(User.role == role)
    
    # 获取总记录数
    total = query.count()
    
    # 分页查询
    users = query.order_by(desc(User.created_at)).offset(skip).limit(limit).all()
    
    return users, total


def create_user(db: Session, user: UserCreate) -> User:
    """
    创建用户
    
    Args:
        db: 数据库会话
        user: 用户创建数据
        
    Returns:
        User: 创建的用户对象
    """
    from app.core.security import get_password_hash
    
    # 密码加密
    hashed_password = get_password_hash(user.password)
    
    # 创建用户对象
    db_user = User(
        username=user.username,
        password=hashed_password,
        email=user.email,
        phone=user.phone,
        real_name=user.real_name,
        role=user.role.value  # 枚举值转字符串
    )
    
    # 添加到数据库
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    return db_user


def update_user(db: Session, user_id: int, user_update: UserUpdate) -> Optional[User]:
    """
    更新用户信息
    
    Args:
        db: 数据库会话
        user_id: 用户ID
        user_update: 更新数据
        
    Returns:
        User: 更新后的用户对象，不存在返回None
    """
    # 查询用户
    db_user = get_user(db, user_id)
    if not db_user:
        return None
    
    # 获取非空字段进行更新
    update_data = user_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_user, key, value)
    
    # 提交更新
    db.commit()
    db.refresh(db_user)
    
    return db_user


def delete_user(db: Session, user_id: int) -> bool:
    """
    删除用户（软删除）
    
    Args:
        db: 数据库会话
        user_id: 用户ID
        
    Returns:
        bool: 删除成功返回True，失败返回False
    """
    # 查询用户
    db_user = get_user(db, user_id)
    if not db_user:
        return False
    
    # 软删除
    db_user.is_deleted = True
    db.commit()
    
    return True


# ==================== 宠物 CRUD 操作 ====================

def get_pet(db: Session, pet_id: int) -> Optional[Pet]:
    """
    根据ID获取宠物
    
    Args:
        db: 数据库会话
        pet_id: 宠物ID
        
    Returns:
        Pet: 宠物对象，不存在返回None
    """
    return db.query(Pet).filter(Pet.id == pet_id, Pet.is_deleted == False).first()


def get_pets(
    db: Session,
    owner_id: Optional[int] = None,
    skip: int = 0,
    limit: int = 10,
    name: Optional[str] = None,
    species: Optional[str] = None,
    gender: Optional[str] = None
) -> Tuple[List[Pet], int]:
    """
    获取宠物列表（分页+筛选）
    
    Args:
        db: 数据库会话
        owner_id: 主人ID（筛选指定主人的宠物）
        skip: 跳过记录数
        limit: 返回记录数
        name: 宠物名称（模糊查询）
        species: 物种筛选
        gender: 性别筛选
        
    Returns:
        Tuple[List[Pet], int]: 宠物列表和总记录数
    """
    # 构建查询
    query = db.query(Pet).filter(Pet.is_deleted == False)
    
    # 主人筛选
    if owner_id:
        query = query.filter(Pet.owner_id == owner_id)
    
    # 名称模糊查询
    if name:
        query = query.filter(Pet.name.like(f"%{name}%"))
    
    # 物种筛选
    if species:
        query = query.filter(Pet.species == species)
    
    # 性别筛选
    if gender:
        query = query.filter(Pet.gender == gender)
    
    # 获取总记录数
    total = query.count()
    
    # 分页查询
    pets = query.order_by(desc(Pet.created_at)).offset(skip).limit(limit).all()
    
    return pets, total


def create_pet(db: Session, pet: PetCreate, owner_id: int) -> Pet:
    """
    创建宠物
    
    Args:
        db: 数据库会话
        pet: 宠物创建数据
        owner_id: 主人ID
        
    Returns:
        Pet: 创建的宠物对象
    """
    # 创建宠物对象
    db_pet = Pet(
        owner_id=owner_id,
        name=pet.name,
        species=pet.species,
        breed=pet.breed,
        gender=pet.gender.value,  # 枚举值转字符串
        birth_date=pet.birth_date,
        weight=pet.weight,
        color=pet.color,
        health_status=pet.health_status,
        special_notes=pet.special_notes
    )
    
    # 添加到数据库
    db.add(db_pet)
    db.commit()
    db.refresh(db_pet)
    
    return db_pet


def update_pet(db: Session, pet_id: int, pet_update: PetUpdate) -> Optional[Pet]:
    """
    更新宠物信息
    
    Args:
        db: 数据库会话
        pet_id: 宠物ID
        pet_update: 更新数据
        
    Returns:
        Pet: 更新后的宠物对象，不存在返回None
    """
    # 查询宠物
    db_pet = get_pet(db, pet_id)
    if not db_pet:
        return None
    
    # 获取非空字段进行更新
    update_data = pet_update.model_dump(exclude_unset=True)
    
    # 如果gender字段存在，转换枚举值
    if 'gender' in update_data and update_data['gender']:
        update_data['gender'] = update_data['gender'].value
    
    for key, value in update_data.items():
        setattr(db_pet, key, value)
    
    # 提交更新
    db.commit()
    db.refresh(db_pet)
    
    return db_pet


def delete_pet(db: Session, pet_id: int) -> bool:
    """
    删除宠物（软删除）
    
    Args:
        db: 数据库会话
        pet_id: 宠物ID
        
    Returns:
        bool: 删除成功返回True，失败返回False
    """
    # 查询宠物
    db_pet = get_pet(db, pet_id)
    if not db_pet:
        return False
    
    # 软删除
    db_pet.is_deleted = True
    db.commit()
    
    return True


# ==================== 服务 CRUD 操作 ====================

def get_service(db: Session, service_id: int) -> Optional[Service]:
    """
    根据ID获取服务
    
    Args:
        db: 数据库会话
        service_id: 服务ID
        
    Returns:
        Service: 服务对象，不存在返回None
    """
    return db.query(Service).filter(Service.id == service_id, Service.is_deleted == False).first()


def get_services(
    db: Session,
    skip: int = 0,
    limit: int = 10,
    category: Optional[str] = None,
    is_available: Optional[bool] = None
) -> Tuple[List[Service], int]:
    """
    获取服务列表（分页+筛选）
    
    Args:
        db: 数据库会话
        skip: 跳过记录数
        limit: 返回记录数
        category: 服务类别筛选
        is_available: 是否上架筛选
        
    Returns:
        Tuple[List[Service], int]: 服务列表和总记录数
    """
    # 构建查询
    query = db.query(Service).filter(Service.is_deleted == False)
    
    # 类别筛选
    if category:
        query = query.filter(Service.category == category)
    
    # 上架状态筛选
    if is_available is not None:
        query = query.filter(Service.is_available == is_available)
    
    # 获取总记录数
    total = query.count()
    
    # 分页查询
    services = query.order_by(desc(Service.created_at)).offset(skip).limit(limit).all()
    
    return services, total


def create_service(db: Session, service: ServiceCreate) -> Service:
    """
    创建服务
    
    Args:
        db: 数据库会话
        service: 服务创建数据
        
    Returns:
        Service: 创建的服务对象
    """
    # 创建服务对象
    db_service = Service(
        name=service.name,
        description=service.description,
        category=service.category,
        price=service.price,
        duration=service.duration
    )
    
    # 添加到数据库
    db.add(db_service)
    db.commit()
    db.refresh(db_service)
    
    return db_service


def update_service(db: Session, service_id: int, service_update: ServiceUpdate) -> Optional[Service]:
    """
    更新服务信息
    
    Args:
        db: 数据库会话
        service_id: 服务ID
        service_update: 更新数据
        
    Returns:
        Service: 更新后的服务对象，不存在返回None
    """
    # 查询服务
    db_service = get_service(db, service_id)
    if not db_service:
        return None
    
    # 获取非空字段进行更新
    update_data = service_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_service, key, value)
    
    # 提交更新
    db.commit()
    db.refresh(db_service)
    
    return db_service


def delete_service(db: Session, service_id: int) -> bool:
    """
    删除服务（软删除）
    
    Args:
        db: 数据库会话
        service_id: 服务ID
        
    Returns:
        bool: 删除成功返回True，失败返回False
    """
    # 查询服务
    db_service = get_service(db, service_id)
    if not db_service:
        return False
    
    # 软删除
    db_service.is_deleted = True
    db.commit()
    
    return True


# ==================== 订单 CRUD 操作 ====================

def get_order(db: Session, order_id: int) -> Optional[Order]:
    """
    根据ID获取订单
    
    Args:
        db: 数据库会话
        order_id: 订单ID
        
    Returns:
        Order: 订单对象，不存在返回None
    """
    return db.query(Order).filter(Order.id == order_id, Order.is_deleted == False).first()


def get_orders(
    db: Session,
    user_id: Optional[int] = None,
    pet_id: Optional[int] = None,
    status: Optional[str] = None,
    skip: int = 0,
    limit: int = 10
) -> Tuple[List[Order], int]:
    """
    获取订单列表（分页+筛选）
    
    Args:
        db: 数据库会话
        user_id: 用户ID筛选
        pet_id: 宠物ID筛选
        status: 订单状态筛选
        skip: 跳过记录数
        limit: 返回记录数
        
    Returns:
        Tuple[List[Order], int]: 订单列表和总记录数
    """
    # 构建查询
    query = db.query(Order).filter(Order.is_deleted == False)
    
    # 用户筛选
    if user_id:
        query = query.filter(Order.user_id == user_id)
    
    # 宠物筛选
    if pet_id:
        query = query.filter(Order.pet_id == pet_id)
    
    # 状态筛选
    if status:
        query = query.filter(Order.status == status)
    
    # 获取总记录数
    total = query.count()
    
    # 分页查询
    orders = query.order_by(desc(Order.created_at)).offset(skip).limit(limit).all()
    
    return orders, total


def create_order(db: Session, order: OrderCreate, user_id: int) -> Order:
    """
    创建订单
    
    Args:
        db: 数据库会话
        order: 订单创建数据
        user_id: 用户ID
        
    Returns:
        Order: 创建的订单对象
        
    Raises:
        ValueError: 服务不存在时抛出
    """
    # 查询服务获取价格
    service = get_service(db, order.service_id)
    if not service:
        raise ValueError("服务不存在")
    
    # 创建订单对象
    db_order = Order(
        order_no=generate_order_no(),
        user_id=user_id,
        pet_id=order.pet_id,
        service_id=order.service_id,
        appointment_time=order.appointment_time,
        total_amount=float(service.price),
        notes=order.notes
    )
    
    # 添加到数据库
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    
    return db_order


def update_order(db: Session, order_id: int, order_update: OrderUpdate) -> Optional[Order]:
    """
    更新订单信息
    
    Args:
        db: 数据库会话
        order_id: 订单ID
        order_update: 更新数据
        
    Returns:
        Order: 更新后的订单对象，不存在返回None
    """
    # 查询订单
    db_order = get_order(db, order_id)
    if not db_order:
        return None
    
    # 获取非空字段进行更新
    update_data = order_update.model_dump(exclude_unset=True)
    
    # 如果status字段存在，转换枚举值
    if 'status' in update_data and update_data['status']:
        update_data['status'] = update_data['status'].value
    
    for key, value in update_data.items():
        setattr(db_order, key, value)
    
    # 提交更新
    db.commit()
    db.refresh(db_order)
    
    return db_order


def delete_order(db: Session, order_id: int) -> bool:
    """
    删除订单（软删除）
    
    Args:
        db: 数据库会话
        order_id: 订单ID
        
    Returns:
        bool: 删除成功返回True，失败返回False
    """
    # 查询订单
    db_order = get_order(db, order_id)
    if not db_order:
        return False
    
    # 软删除
    db_order.is_deleted = True
    db.commit()
    
    return True


# ==================== 寄养 CRUD 操作 ====================

def get_boarding(db: Session, boarding_id: int) -> Optional[Boarding]:
    """
    根据ID获取寄养记录
    
    Args:
        db: 数据库会话
        boarding_id: 寄养记录ID
        
    Returns:
        Boarding: 寄养记录对象，不存在返回None
    """
    return db.query(Boarding).filter(Boarding.id == boarding_id, Boarding.is_deleted == False).first()


def get_boardings(
    db: Session,
    staff_id: Optional[int] = None,
    pet_id: Optional[int] = None,
    status: Optional[str] = None,
    skip: int = 0,
    limit: int = 10
) -> Tuple[List[Boarding], int]:
    """
    获取寄养记录列表（分页+筛选）
    
    Args:
        db: 数据库会话
        staff_id: 饲养员ID筛选
        pet_id: 宠物ID筛选
        status: 寄养状态筛选
        skip: 跳过记录数
        limit: 返回记录数
        
    Returns:
        Tuple[List[Boarding], int]: 寄养记录列表和总记录数
    """
    # 构建查询
    query = db.query(Boarding).filter(Boarding.is_deleted == False)
    
    # 饲养员筛选
    if staff_id:
        query = query.filter(Boarding.staff_id == staff_id)
    
    # 宠物筛选
    if pet_id:
        query = query.filter(Boarding.pet_id == pet_id)
    
    # 状态筛选
    if status:
        query = query.filter(Boarding.status == status)
    
    # 获取总记录数
    total = query.count()
    
    # 分页查询
    boardings = query.order_by(desc(Boarding.created_at)).offset(skip).limit(limit).all()
    
    return boardings, total


def create_boarding(db: Session, boarding: BoardingCreate, order_id: int) -> Boarding:
    """
    创建寄养记录
    
    Args:
        db: 数据库会话
        boarding: 寄养创建数据
        order_id: 订单ID
        
    Returns:
        Boarding: 创建的寄养记录对象
    """
    # 创建寄养记录对象
    db_boarding = Boarding(
        order_id=order_id,
        pet_id=boarding.pet_id,
        staff_id=boarding.staff_id,
        start_date=boarding.start_date,
        end_date=boarding.end_date
    )
    
    # 添加到数据库
    db.add(db_boarding)
    db.commit()
    db.refresh(db_boarding)
    
    return db_boarding


def update_boarding(db: Session, boarding_id: int, boarding_update: BoardingUpdate) -> Optional[Boarding]:
    """
    更新寄养记录信息
    
    Args:
        db: 数据库会话
        boarding_id: 寄养记录ID
        boarding_update: 更新数据
        
    Returns:
        Boarding: 更新后的寄养记录对象，不存在返回None
    """
    # 查询寄养记录
    db_boarding = get_boarding(db, boarding_id)
    if not db_boarding:
        return None
    
    # 获取非空字段进行更新
    update_data = boarding_update.model_dump(exclude_unset=True)
    
    # 如果status字段存在，转换枚举值
    if 'status' in update_data and update_data['status']:
        update_data['status'] = update_data['status'].value
    
    for key, value in update_data.items():
        setattr(db_boarding, key, value)
    
    # 提交更新
    db.commit()
    db.refresh(db_boarding)
    
    return db_boarding


def delete_boarding(db: Session, boarding_id: int) -> bool:
    """
    删除寄养记录（软删除）
    
    Args:
        db: 数据库会话
        boarding_id: 寄养记录ID
        
    Returns:
        bool: 删除成功返回True，失败返回False
    """
    # 查询寄养记录
    db_boarding = get_boarding(db, boarding_id)
    if not db_boarding:
        return False
    
    # 软删除
    db_boarding.is_deleted = True
    db.commit()
    
    return True


# ==================== 健康记录 CRUD 操作 ====================

def get_health_record(db: Session, record_id: int) -> Optional[HealthRecord]:
    """
    根据ID获取健康记录
    
    Args:
        db: 数据库会话
        record_id: 健康记录ID
        
    Returns:
        HealthRecord: 健康记录对象，不存在返回None
    """
    return db.query(HealthRecord).filter(
        HealthRecord.id == record_id,
        HealthRecord.is_deleted == False
    ).first()


def get_health_records(
    db: Session,
    pet_id: Optional[int] = None,
    vet_id: Optional[int] = None,
    record_type: Optional[str] = None,
    skip: int = 0,
    limit: int = 10
) -> Tuple[List[HealthRecord], int]:
    """
    获取健康记录列表（分页+筛选）
    
    Args:
        db: 数据库会话
        pet_id: 宠物ID筛选
        vet_id: 兽医ID筛选
        record_type: 记录类型筛选
        skip: 跳过记录数
        limit: 返回记录数
        
    Returns:
        Tuple[List[HealthRecord], int]: 健康记录列表和总记录数
    """
    # 构建查询
    query = db.query(HealthRecord).filter(HealthRecord.is_deleted == False)
    
    # 宠物筛选
    if pet_id:
        query = query.filter(HealthRecord.pet_id == pet_id)
    
    # 兽医筛选
    if vet_id:
        query = query.filter(HealthRecord.vet_id == vet_id)
    
    # 类型筛选
    if record_type:
        query = query.filter(HealthRecord.type == record_type)
    
    # 获取总记录数
    total = query.count()
    
    # 分页查询
    records = query.order_by(desc(HealthRecord.check_date)).offset(skip).limit(limit).all()
    
    return records, total


def create_health_record(db: Session, record: HealthRecordCreate) -> HealthRecord:
    """
    创建健康记录
    
    Args:
        db: 数据库会话
        record: 健康记录创建数据
        
    Returns:
        HealthRecord: 创建的健康记录对象
    """
    # 创建健康记录对象
    db_record = HealthRecord(
        pet_id=record.pet_id,
        vet_id=record.vet_id,
        check_date=record.check_date,
        type=record.type.value,  # 枚举值转字符串
        description=record.description,
        diagnosis=record.diagnosis,
        prescription=record.prescription,
        notes=record.notes
    )
    
    # 添加到数据库
    db.add(db_record)
    db.commit()
    db.refresh(db_record)
    
    return db_record


def update_health_record(db: Session, record_id: int, record_update: HealthRecordUpdate) -> Optional[HealthRecord]:
    """
    更新健康记录信息
    
    Args:
        db: 数据库会话
        record_id: 健康记录ID
        record_update: 更新数据
        
    Returns:
        HealthRecord: 更新后的健康记录对象，不存在返回None
    """
    # 查询健康记录
    db_record = get_health_record(db, record_id)
    if not db_record:
        return None
    
    # 获取非空字段进行更新
    update_data = record_update.model_dump(exclude_unset=True)
    
    # 如果type字段存在，转换枚举值
    if 'type' in update_data and update_data['type']:
        update_data['type'] = update_data['type'].value
    
    for key, value in update_data.items():
        setattr(db_record, key, value)
    
    # 提交更新
    db.commit()
    db.refresh(db_record)
    
    return db_record


def delete_health_record(db: Session, record_id: int) -> bool:
    """
    删除健康记录（软删除）
    
    Args:
        db: 数据库会话
        record_id: 健康记录ID
        
    Returns:
        bool: 删除成功返回True，失败返回False
    """
    # 查询健康记录
    db_record = get_health_record(db, record_id)
    if not db_record:
        return False
    
    # 软删除
    db_record.is_deleted = True
    db.commit()
    
    return True


# ==================== 统计查询操作 ====================

def get_dashboard_stats(db: Session) -> dict:
    """
    获取仪表盘统计数据
    
    Args:
        db: 数据库会话
        
    Returns:
        dict: 统计数据字典
    """
    # 总用户数
    total_users = db.query(func.count(User.id)).filter(User.is_deleted == False).scalar()
    
    # 总宠物数
    total_pets = db.query(func.count(Pet.id)).filter(Pet.is_deleted == False).scalar()
    
    # 总订单数
    total_orders = db.query(func.count(Order.id)).filter(Order.is_deleted == False).scalar()
    
    # 总营收（已完成订单的总金额）
    total_revenue = db.query(func.sum(Order.total_amount)).filter(
        Order.is_deleted == False,
        Order.status == "completed"
    ).scalar() or 0
    
    # 进行中订单数（已确认和进行中的订单）
    active_orders = db.query(func.count(Order.id)).filter(
        Order.is_deleted == False,
        Order.status.in_(["confirmed", "in_progress"])
    ).scalar()
    
    return {
        "total_users": total_users,
        "total_pets": total_pets,
        "total_orders": total_orders,
        "total_revenue": float(total_revenue),
        "active_orders": active_orders
    }
