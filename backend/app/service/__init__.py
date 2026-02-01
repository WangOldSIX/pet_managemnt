"""
业务逻辑层 (Service Layer)
处理业务逻辑，调用CRUD层完成数据库操作
"""

from typing import List, Optional, Tuple
from sqlalchemy.orm import Session
from app.crud import (
    # 用户 CRUD
    get_user, get_user_by_username, get_users, create_user, update_user, delete_user,
    # 宠物 CRUD
    get_pet, get_pets, create_pet, update_pet, delete_pet,
    # 服务 CRUD
    get_service, get_services, create_service, update_service, delete_service,
    # 订单 CRUD
    get_order, get_orders, create_order, update_order, delete_order,
    # 寄养 CRUD
    get_boarding, get_boardings, create_boarding, update_boarding, delete_boarding,
    # 健康记录 CRUD
    get_health_record, get_health_records, create_health_record, update_health_record, delete_health_record,
    # 统计
    get_dashboard_stats
)
from app.db.models import User
from app.core.security import verify_password
from app.schemas import (
    UserCreate, UserUpdate,
    PetCreate, PetUpdate,
    ServiceCreate, ServiceUpdate,
    OrderCreate, OrderUpdate,
    BoardingCreate, BoardingUpdate,
    HealthRecordCreate, HealthRecordUpdate
)
from app.core.exceptions import NotFoundError, ValidationError, ConflictError


# ==================== 用户服务 ====================

class UserService:
    """用户服务类，处理用户相关业务逻辑"""
    
    @staticmethod
    def authenticate(db: Session, username: str, password: str) -> Optional[User]:
        """
        用户认证
        
        Args:
            db: 数据库会话
            username: 用户名
            password: 密码
            
        Returns:
            User: 认证成功返回用户对象，失败返回None
        """
        user = get_user_by_username(db, username)
        if not user or not verify_password(password, user.password):
            return None
        return user
    
    @staticmethod
    def get_user_detail(db: Session, user_id: int) -> User:
        """
        获取用户详情
        
        Args:
            db: 数据库会话
            user_id: 用户ID
            
        Returns:
            User: 用户对象
            
        Raises:
            NotFoundError: 用户不存在时抛出
        """
        user = get_user(db, user_id)
        if not user:
            raise NotFoundError("用户不存在")
        return user
    
    @staticmethod
    def get_user_list(
        db: Session,
        page: int = 1,
        size: int = 10,
        username: Optional[str] = None,
        role: Optional[str] = None
    ) -> Tuple[List[User], int]:
        """
        获取用户列表（分页）
        
        Args:
            db: 数据库会话
            page: 页码
            size: 每页数量
            username: 用户名筛选
            role: 角色筛选
            
        Returns:
            Tuple[List[User], int]: 用户列表和总记录数
        """
        skip = (page - 1) * size
        return get_users(db, skip, size, username, role)
    
    @staticmethod
    def register(db: Session, user: UserCreate) -> User:
        """
        用户注册
        
        Args:
            db: 数据库会话
            user: 用户创建数据
            
        Returns:
            User: 创建的用户对象
            
        Raises:
            ConflictError: 用户名已存在时抛出
        """
        # 检查用户名是否已存在
        existing_user = get_user_by_username(db, user.username)
        if existing_user:
            raise ConflictError("用户名已存在")
        
        return create_user(db, user)
    
    @staticmethod
    def update_user_info(db: Session, user_id: int, user_update: UserUpdate) -> User:
        """
        更新用户信息
        
        Args:
            db: 数据库会话
            user_id: 用户ID
            user_update: 更新数据
            
        Returns:
            User: 更新后的用户对象
            
        Raises:
            NotFoundError: 用户不存在时抛出
        """
        user = update_user(db, user_id, user_update)
        if not user:
            raise NotFoundError("用户不存在")
        return user
    
    @staticmethod
    def remove_user(db: Session, user_id: int) -> bool:
        """
        删除用户
        
        Args:
            db: 数据库会话
            user_id: 用户ID
            
        Returns:
            bool: 删除成功返回True
            
        Raises:
            NotFoundError: 用户不存在时抛出
        """
        success = delete_user(db, user_id)
        if not success:
            raise NotFoundError("用户不存在")
        return True


# ==================== 宠物服务 ====================

class PetService:
    """宠物服务类，处理宠物相关业务逻辑"""
    
    @staticmethod
    def get_pet_detail(db: Session, pet_id: int):
        """
        获取宠物详情
        
        Args:
            db: 数据库会话
            pet_id: 宠物ID
            
        Returns:
            Pet: 宠物对象
            
        Raises:
            NotFoundError: 宠物不存在时抛出
        """
        pet = get_pet(db, pet_id)
        if not pet:
            raise NotFoundError("宠物不存在")
        return pet
    
    @staticmethod
    def get_pet_list(
        db: Session,
        owner_id: Optional[int] = None,
        page: int = 1,
        size: int = 10,
        name: Optional[str] = None,
        species: Optional[str] = None,
        gender: Optional[str] = None
    ) -> Tuple[List, int]:
        """
        获取宠物列表（分页）
        
        Args:
            db: 数据库会话
            owner_id: 主人ID
            page: 页码
            size: 每页数量
            name: 宠物名称筛选
            species: 物种筛选
            gender: 性别筛选
            
        Returns:
            Tuple[List[Pet], int]: 宠物列表和总记录数
        """
        skip = (page - 1) * size
        return get_pets(db, owner_id, skip, size, name, species, gender)
    
    @staticmethod
    def create_pet_info(db: Session, pet: PetCreate, owner_id: int):
        """
        创建宠物
        
        Args:
            db: 数据库会话
            pet: 宠物创建数据
            owner_id: 主人ID
            
        Returns:
            Pet: 创建的宠物对象
        """
        return create_pet(db, pet, owner_id)
    
    @staticmethod
    def update_pet_info(db: Session, pet_id: int, pet_update: PetUpdate):
        """
        更新宠物信息
        
        Args:
            db: 数据库会话
            pet_id: 宠物ID
            pet_update: 更新数据
            
        Returns:
            Pet: 更新后的宠物对象
            
        Raises:
            NotFoundError: 宠物不存在时抛出
        """
        pet = update_pet(db, pet_id, pet_update)
        if not pet:
            raise NotFoundError("宠物不存在")
        return pet
    
    @staticmethod
    def remove_pet(db: Session, pet_id: int) -> bool:
        """
        删除宠物
        
        Args:
            db: 数据库会话
            pet_id: 宠物ID
            
        Returns:
            bool: 删除成功返回True
            
        Raises:
            NotFoundError: 宠物不存在时抛出
        """
        success = delete_pet(db, pet_id)
        if not success:
            raise NotFoundError("宠物不存在")
        return True


# ==================== 服务服务 ====================

class ServiceService:
    """服务服务类，处理服务相关业务逻辑"""
    
    @staticmethod
    def get_service_detail(db: Session, service_id: int):
        """
        获取服务详情
        
        Args:
            db: 数据库会话
            service_id: 服务ID
            
        Returns:
            Service: 服务对象
            
        Raises:
            NotFoundError: 服务不存在时抛出
        """
        service = get_service(db, service_id)
        if not service:
            raise NotFoundError("服务不存在")
        return service
    
    @staticmethod
    def get_service_list(
        db: Session,
        page: int = 1,
        size: int = 10,
        category: Optional[str] = None,
        is_available: Optional[bool] = None
    ) -> Tuple[List, int]:
        """
        获取服务列表（分页）
        
        Args:
            db: 数据库会话
            page: 页码
            size: 每页数量
            category: 服务类别筛选
            is_available: 是否上架筛选
            
        Returns:
            Tuple[List[Service], int]: 服务列表和总记录数
        """
        skip = (page - 1) * size
        return get_services(db, skip, size, category, is_available)
    
    @staticmethod
    def create_service_info(db: Session, service: ServiceCreate):
        """
        创建服务
        
        Args:
            db: 数据库会话
            service: 服务创建数据
            
        Returns:
            Service: 创建的服务对象
        """
        return create_service(db, service)
    
    @staticmethod
    def update_service_info(db: Session, service_id: int, service_update: ServiceUpdate):
        """
        更新服务信息
        
        Args:
            db: 数据库会话
            service_id: 服务ID
            service_update: 更新数据
            
        Returns:
            Service: 更新后的服务对象
            
        Raises:
            NotFoundError: 服务不存在时抛出
        """
        service = update_service(db, service_id, service_update)
        if not service:
            raise NotFoundError("服务不存在")
        return service
    
    @staticmethod
    def remove_service(db: Session, service_id: int) -> bool:
        """
        删除服务
        
        Args:
            db: 数据库会话
            service_id: 服务ID
            
        Returns:
            bool: 删除成功返回True
            
        Raises:
            NotFoundError: 服务不存在时抛出
        """
        success = delete_service(db, service_id)
        if not success:
            raise NotFoundError("服务不存在")
        return True


# ==================== 订单服务 ====================

class OrderService:
    """订单服务类，处理订单相关业务逻辑"""
    
    @staticmethod
    def get_order_detail(db: Session, order_id: int):
        """
        获取订单详情
        
        Args:
            db: 数据库会话
            order_id: 订单ID
            
        Returns:
            Order: 订单对象
            
        Raises:
            NotFoundError: 订单不存在时抛出
        """
        order = get_order(db, order_id)
        if not order:
            raise NotFoundError("订单不存在")
        return order
    
    @staticmethod
    def get_order_list(
        db: Session,
        user_id: Optional[int] = None,
        pet_id: Optional[int] = None,
        status: Optional[str] = None,
        page: int = 1,
        size: int = 10
    ) -> Tuple[List, int]:
        """
        获取订单列表（分页）
        
        Args:
            db: 数据库会话
            user_id: 用户ID筛选
            pet_id: 宠物ID筛选
            status: 订单状态筛选
            page: 页码
            size: 每页数量
            
        Returns:
            Tuple[List[Order], int]: 订单列表和总记录数
        """
        skip = (page - 1) * size
        return get_orders(db, user_id, pet_id, status, skip, size)
    
    @staticmethod
    def create_order_info(db: Session, order: OrderCreate, user_id: int):
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
        return create_order(db, order, user_id)
    
    @staticmethod
    def update_order_info(db: Session, order_id: int, order_update: OrderUpdate):
        """
        更新订单信息
        
        Args:
            db: 数据库会话
            order_id: 订单ID
            order_update: 更新数据
            
        Returns:
            Order: 更新后的订单对象
            
        Raises:
            NotFoundError: 订单不存在时抛出
        """
        order = update_order(db, order_id, order_update)
        if not order:
            raise NotFoundError("订单不存在")
        return order
    
    @staticmethod
    def remove_order(db: Session, order_id: int) -> bool:
        """
        删除订单
        
        Args:
            db: 数据库会话
            order_id: 订单ID
            
        Returns:
            bool: 删除成功返回True
            
        Raises:
            NotFoundError: 订单不存在时抛出
        """
        success = delete_order(db, order_id)
        if not success:
            raise NotFoundError("订单不存在")
        return True


# ==================== 寄养服务 ====================

class BoardingService:
    """寄养服务类，处理寄养相关业务逻辑"""
    
    @staticmethod
    def get_boarding_detail(db: Session, boarding_id: int):
        """
        获取寄养详情
        
        Args:
            db: 数据库会话
            boarding_id: 寄养记录ID
            
        Returns:
            Boarding: 寄养记录对象
            
        Raises:
            NotFoundError: 寄养记录不存在时抛出
        """
        boarding = get_boarding(db, boarding_id)
        if not boarding:
            raise NotFoundError("寄养记录不存在")
        return boarding
    
    @staticmethod
    def get_boarding_list(
        db: Session,
        staff_id: Optional[int] = None,
        pet_id: Optional[int] = None,
        status: Optional[str] = None,
        page: int = 1,
        size: int = 10
    ) -> Tuple[List, int]:
        """
        获取寄养记录列表（分页）
        
        Args:
            db: 数据库会话
            staff_id: 饲养员ID筛选
            pet_id: 宠物ID筛选
            status: 寄养状态筛选
            page: 页码
            size: 每页数量
            
        Returns:
            Tuple[List[Boarding], int]: 寄养记录列表和总记录数
        """
        skip = (page - 1) * size
        return get_boardings(db, staff_id, pet_id, status, skip, size)
    
    @staticmethod
    def create_boarding_info(db: Session, boarding: BoardingCreate, order_id: int):
        """
        创建寄养记录
        
        Args:
            db: 数据库会话
            boarding: 寄养创建数据
            order_id: 订单ID
            
        Returns:
            Boarding: 创建的寄养记录对象
        """
        return create_boarding(db, boarding, order_id)
    
    @staticmethod
    def update_boarding_info(db: Session, boarding_id: int, boarding_update: BoardingUpdate):
        """
        更新寄养记录信息
        
        Args:
            db: 数据库会话
            boarding_id: 寄养记录ID
            boarding_update: 更新数据
            
        Returns:
            Boarding: 更新后的寄养记录对象
            
        Raises:
            NotFoundError: 寄养记录不存在时抛出
        """
        boarding = update_boarding(db, boarding_id, boarding_update)
        if not boarding:
            raise NotFoundError("寄养记录不存在")
        return boarding
    
    @staticmethod
    def remove_boarding(db: Session, boarding_id: int) -> bool:
        """
        删除寄养记录
        
        Args:
            db: 数据库会话
            boarding_id: 寄养记录ID
            
        Returns:
            bool: 删除成功返回True
            
        Raises:
            NotFoundError: 寄养记录不存在时抛出
        """
        success = delete_boarding(db, boarding_id)
        if not success:
            raise NotFoundError("寄养记录不存在")
        return True


# ==================== 健康记录服务 ====================

class HealthRecordService:
    """健康记录服务类，处理健康记录相关业务逻辑"""
    
    @staticmethod
    def get_health_record_detail(db: Session, record_id: int):
        """
        获取健康记录详情
        
        Args:
            db: 数据库会话
            record_id: 健康记录ID
            
        Returns:
            HealthRecord: 健康记录对象
            
        Raises:
            NotFoundError: 健康记录不存在时抛出
        """
        record = get_health_record(db, record_id)
        if not record:
            raise NotFoundError("健康记录不存在")
        return record
    
    @staticmethod
    def get_health_record_list(
        db: Session,
        pet_id: Optional[int] = None,
        vet_id: Optional[int] = None,
        record_type: Optional[str] = None,
        page: int = 1,
        size: int = 10
    ) -> Tuple[List, int]:
        """
        获取健康记录列表（分页）
        
        Args:
            db: 数据库会话
            pet_id: 宠物ID筛选
            vet_id: 兽医ID筛选
            record_type: 记录类型筛选
            page: 页码
            size: 每页数量
            
        Returns:
            Tuple[List[HealthRecord], int]: 健康记录列表和总记录数
        """
        skip = (page - 1) * size
        return get_health_records(db, pet_id, vet_id, record_type, skip, size)
    
    @staticmethod
    def create_health_record_info(db: Session, record: HealthRecordCreate):
        """
        创建健康记录
        
        Args:
            db: 数据库会话
            record: 健康记录创建数据
            
        Returns:
            HealthRecord: 创建的健康记录对象
        """
        return create_health_record(db, record)
    
    @staticmethod
    def update_health_record_info(db: Session, record_id: int, record_update: HealthRecordUpdate):
        """
        更新健康记录信息
        
        Args:
            db: 数据库会话
            record_id: 健康记录ID
            record_update: 更新数据
            
        Returns:
            HealthRecord: 更新后的健康记录对象
            
        Raises:
            NotFoundError: 健康记录不存在时抛出
        """
        record = update_health_record(db, record_id, record_update)
        if not record:
            raise NotFoundError("健康记录不存在")
        return record
    
    @staticmethod
    def remove_health_record(db: Session, record_id: int) -> bool:
        """
        删除健康记录
        
        Args:
            db: 数据库会话
            record_id: 健康记录ID
            
        Returns:
            bool: 删除成功返回True
            
        Raises:
            NotFoundError: 健康记录不存在时抛出
        """
        success = delete_health_record(db, record_id)
        if not success:
            raise NotFoundError("健康记录不存在")
        return True


# ==================== 仪表盘服务 ====================

class DashboardService:
    """仪表盘服务类，处理统计数据相关业务逻辑"""
    
    @staticmethod
    def get_stats(db: Session) -> dict:
        """
        获取统计数据
        
        Args:
            db: 数据库会话
            
        Returns:
            dict: 统计数据字典
        """
        return get_dashboard_stats(db)
