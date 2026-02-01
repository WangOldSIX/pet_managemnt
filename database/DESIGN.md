# 宠物管理系统数据库设计说明

## 一、数据库概述

本系统采用 MySQL 8.0 数据库，遵循第三范式设计原则，实现宠物管理业务的完整数据存储。

### 1.1 设计原则
- **第三范式**：消除传递依赖，每个字段直接依赖于主键
- **命名规范**：表名和字段名使用下划线命名法，符合数据库规范
- **软删除**：所有表包含 `is_deleted` 字段，实现数据的安全删除
- **时间戳**：所有表包含 `created_at` 和 `updated_at` 字段，记录数据的创建和修改时间
- **索引优化**：在常用查询字段和连接字段上创建索引，提升查询性能

## 二、表结构设计

### 2.1 用户表 (users)

#### 字段说明
| 字段名 | 类型 | 约束 | 说明 |
|--------|------|------|------|
| id | BIGINT UNSIGNED | PK, AUTO_INCREMENT | 用户ID，主键，自增 |
| username | VARCHAR(50) | NOT NULL, UNIQUE | 用户名，唯一，用于登录 |
| password | VARCHAR(255) | NOT NULL | 密码，bcrypt加密存储 |
| email | VARCHAR(100) | NULL, INDEX | 邮箱地址 |
| phone | VARCHAR(20) | NULL, INDEX | 手机号 |
| real_name | VARCHAR(50) | NULL | 真实姓名 |
| role | ENUM | NOT NULL | 角色：admin-管理员，owner-宠物主人，staff-员工 |
| avatar | VARCHAR(255) | NULL | 头像URL |
| is_active | TINYINT(1) | NOT NULL, DEFAULT 1 | 是否启用 |
| is_deleted | TINYINT(1) | NOT NULL, DEFAULT 0 | 是否删除（软删除） |
| created_at | DATETIME | NOT NULL, DEFAULT CURRENT_TIMESTAMP | 创建时间 |
| updated_at | DATETIME | NOT NULL, ON UPDATE CURRENT_TIMESTAMP | 更新时间 |

#### 索引设计
- 主键索引：`PRIMARY KEY (id)`
- 唯一索引：`UNIQUE KEY uk_username (username)` - 保证用户名唯一
- 普通索引：`idx_email (email)` - 加速邮箱查询
- 普通索引：`idx_phone (phone)` - 加速手机号查询
- 普通索引：`idx_role (role)` - 加速角色筛选
- 普通索引：`idx_created_at (created_at)` - 加速时间范围查询

### 2.2 宠物档案表 (pets)

#### 字段说明
| 字段名 | 类型 | 约束 | 说明 |
|--------|------|------|------|
| id | BIGINT UNSIGNED | PK, AUTO_INCREMENT | 宠物ID，主键，自增 |
| owner_id | BIGINT UNSIGNED | NOT NULL, FK | 主人ID，外键关联users表 |
| name | VARCHAR(50) | NOT NULL | 宠物名称 |
| species | VARCHAR(50) | NOT NULL, INDEX | 物种：猫、狗、其他 |
| breed | VARCHAR(50) | NULL | 品种 |
| gender | ENUM | NOT NULL | 性别：male-公，female-母 |
| birth_date | DATE | NULL | 出生日期 |
| weight | DECIMAL(5,2) | NULL | 体重，单位kg |
| color | VARCHAR(50) | NULL | 毛色 |
| health_status | TEXT | NULL | 健康状况描述 |
| special_notes | TEXT | NULL | 特殊备注 |
| avatar | VARCHAR(255) | NULL | 宠物照片URL |
| is_deleted | TINYINT(1) | NOT NULL, DEFAULT 0 | 是否删除（软删除） |
| created_at | DATETIME | NOT NULL, DEFAULT CURRENT_TIMESTAMP | 创建时间 |
| updated_at | DATETIME | NOT NULL, ON UPDATE CURRENT_TIMESTAMP | 更新时间 |

#### 索引设计
- 主键索引：`PRIMARY KEY (id)`
- 外键索引：`idx_owner_id (owner_id)` - 加速主人查询
- 普通索引：`idx_species (species)` - 加速物种筛选
- 普通索引：`idx_gender (gender)` - 加速性别筛选

### 2.3 宠物服务表 (services)

#### 字段说明
| 字段名 | 类型 | 约束 | 说明 |
|--------|------|------|------|
| id | BIGINT UNSIGNED | PK, AUTO_INCREMENT | 服务ID，主键，自增 |
| name | VARCHAR(100) | NOT NULL | 服务名称 |
| description | TEXT | NULL | 服务详细描述 |
| category | VARCHAR(50) | NOT NULL, INDEX | 服务类别：美容、医疗、寄养、训练等 |
| price | DECIMAL(10,2) | NOT NULL, INDEX | 服务价格，单位元 |
| duration | INT | NULL | 服务时长，单位分钟 |
| image | VARCHAR(255) | NULL | 服务图片URL |
| is_available | TINYINT(1) | NOT NULL, DEFAULT 1, INDEX | 是否上架：1-上架，0-下架 |
| is_deleted | TINYINT(1) | NOT NULL, DEFAULT 0 | 是否删除（软删除） |
| created_at | DATETIME | NOT NULL, DEFAULT CURRENT_TIMESTAMP | 创建时间 |
| updated_at | DATETIME | NOT NULL, ON UPDATE CURRENT_TIMESTAMP | 更新时间 |

#### 索引设计
- 主键索引：`PRIMARY KEY (id)`
- 普通索引：`idx_category (category)` - 加速类别筛选
- 普通索引：`idx_available (is_available)` - 加速上架状态查询
- 普通索引：`idx_price (price)` - 加速价格范围查询

### 2.4 订单表 (orders)

#### 字段说明
| 字段名 | 类型 | 约束 | 说明 |
|--------|------|------|------|
| id | BIGINT UNSIGNED | PK, AUTO_INCREMENT | 订单ID，主键，自增 |
| order_no | VARCHAR(50) | NOT NULL, UNIQUE, INDEX | 订单号，唯一 |
| user_id | BIGINT UNSIGNED | NOT NULL, FK, INDEX | 用户ID，外键关联users表 |
| pet_id | BIGINT UNSIGNED | NOT NULL, FK, INDEX | 宠物ID，外键关联pets表 |
| service_id | BIGINT UNSIGNED | NOT NULL, FK, INDEX | 服务ID，外键关联services表 |
| staff_id | BIGINT UNSIGNED | NULL, FK, INDEX | 服务员工ID，外键关联users表 |
| appointment_time | DATETIME | NULL, INDEX | 预约时间 |
| status | ENUM | NOT NULL, DEFAULT 'pending', INDEX | 订单状态 |
| total_amount | DECIMAL(10,2) | NOT NULL | 订单总额 |
| notes | TEXT | NULL | 订单备注 |
| is_deleted | TINYINT(1) | NOT NULL, DEFAULT 0 | 是否删除（软删除） |
| created_at | DATETIME | NOT NULL, DEFAULT CURRENT_TIMESTAMP | 创建时间 |
| updated_at | DATETIME | NOT NULL, ON UPDATE CURRENT_TIMESTAMP | 更新时间 |

#### 索引设计
- 主键索引：`PRIMARY KEY (id)`
- 唯一索引：`UNIQUE KEY uk_order_no (order_no)` - 保证订单号唯一
- 外键索引：`idx_user_id (user_id)` - 加速用户订单查询
- 外键索引：`idx_pet_id (pet_id)` - 加速宠物订单查询
- 外键索引：`idx_service_id (service_id)` - 加速服务订单查询
- 外键索引：`idx_staff_id (staff_id)` - 加速员工订单查询
- 普通索引：`idx_status (status)` - 加速状态筛选
- 普通索引：`idx_appointment_time (appointment_time)` - 加速时间范围查询

### 2.5 寄养表 (boardings)

#### 字段说明
| 字段名 | 类型 | 约束 | 说明 |
|--------|------|------|------|
| id | BIGINT UNSIGNED | PK, AUTO_INCREMENT | 寄养ID，主键，自增 |
| order_id | BIGINT UNSIGNED | NOT NULL, FK, INDEX | 订单ID，外键关联orders表 |
| pet_id | BIGINT UNSIGNED | NOT NULL, FK, INDEX | 宠物ID，外键关联pets表 |
| staff_id | BIGINT UNSIGNED | NOT NULL, FK, INDEX | 饲养员ID，外键关联users表 |
| start_date | DATETIME | NOT NULL, INDEX | 寄养开始时间 |
| end_date | DATETIME | NOT NULL, INDEX | 寄养结束时间 |
| status | ENUM | NOT NULL, DEFAULT 'scheduled', INDEX | 寄养状态 |
| daily_notes | TEXT | NULL | 每日记录 |
| food_type | VARCHAR(100) | NULL | 食物类型 |
| feeding_schedule | VARCHAR(100) | NULL | 喂食计划 |
| is_deleted | TINYINT(1) | NOT NULL, DEFAULT 0 | 是否删除（软删除） |
| created_at | DATETIME | NOT NULL, DEFAULT CURRENT_TIMESTAMP | 创建时间 |
| updated_at | DATETIME | NOT NULL, ON UPDATE CURRENT_TIMESTAMP | 更新时间 |

#### 索引设计
- 主键索引：`PRIMARY KEY (id)`
- 外键索引：`idx_order_id (order_id)` - 加速订单查询
- 外键索引：`idx_pet_id (pet_id)` - 加速宠物寄养查询
- 外键索引：`idx_staff_id (staff_id)` - 加速饲养员查询
- 复合索引：`idx_dates (start_date, end_date)` - 加速时间范围查询
- 普通索引：`idx_status (status)` - 加速状态筛选

### 2.6 健康记录表 (health_records)

#### 字段说明
| 字段名 | 类型 | 约束 | 说明 |
|--------|------|------|------|
| id | BIGINT UNSIGNED | PK, AUTO_INCREMENT | 健康记录ID，主键，自增 |
| pet_id | BIGINT UNSIGNED | NOT NULL, FK, INDEX | 宠物ID，外键关联pets表 |
| vet_id | BIGINT UNSIGNED | NOT NULL, FK, INDEX | 兽医ID，外键关联users表 |
| check_date | DATETIME | NOT NULL, INDEX | 检查日期 |
| type | ENUM | NOT NULL, INDEX | 记录类型：检查、治疗、疫苗、手术 |
| description | TEXT | NULL | 详细描述 |
| diagnosis | TEXT | NULL | 诊断结果 |
| prescription | TEXT | NULL | 处方信息 |
| notes | TEXT | NULL | 备注 |
| is_deleted | TINYINT(1) | NOT NULL, DEFAULT 0 | 是否删除（软删除） |
| created_at | DATETIME | NOT NULL, DEFAULT CURRENT_TIMESTAMP | 创建时间 |
| updated_at | DATETIME | NOT NULL, ON UPDATE CURRENT_TIMESTAMP | 更新时间 |

#### 索引设计
- 主键索引：`PRIMARY KEY (id)`
- 外键索引：`idx_pet_id (pet_id)` - 加速宠物健康记录查询
- 外键索引：`idx_vet_id (vet_id)` - 加速兽医记录查询
- 普通索引：`idx_check_date (check_date)` - 加速时间范围查询
- 普通索引：`idx_type (type)` - 加速类型筛选

## 三、表关系说明

### 3.1 表间关系图（文字描述）

```
users (用户表)
├── 1:N → pets (宠物档案表) - 一个用户可以拥有多只宠物
├── 1:N → orders (订单表) - 一个用户可以有多个订单
├── 1:N → boardings (寄养表) - 一个员工可以负责多个寄养
├── 1:N → health_records (健康记录表) - 一个兽医可以有多条健康记录

pets (宠物档案表)
├── N:1 → users (用户表) - 多只宠物属于一个用户
├── 1:N → orders (订单表) - 一只宠物可以有多个订单
├── 1:N → boardings (寄养表) - 一只宠物可以有多条寄养记录
└── 1:N → health_records (健康记录表) - 一只宠物可以有多条健康记录

services (服务表)
└── 1:N → orders (订单表) - 一个服务可以出现在多个订单中

orders (订单表)
├── N:1 → users (用户表) - 多个订单属于一个用户（订单发起者）
├── N:1 → users (用户表) - 多个订单可以由一个员工服务
├── N:1 → pets (宠物档案表) - 多个订单针对一只宠物
├── N:1 → services (服务表) - 多个订单对应一个服务
└── 1:N → boardings (寄养表) - 一个订单可以对应一条寄养记录

boardings (寄养表)
├── N:1 → orders (订单表) - 多条寄养记录属于一个订单
├── N:1 → pets (宠物档案表) - 多条寄养记录针对一只宠物
└── N:1 → users (用户表) - 多条寄养记录由一个员工负责

health_records (健康记录表)
├── N:1 → pets (宠物档案表) - 多条健康记录针对一只宠物
└── N:1 → users (用户表) - 多条健康记录由一个兽医创建
```

### 3.2 外键约束说明

| 外键名称 | 主表 | 主字段 | 从表 | 从字段 | 级联规则 | 说明 |
|----------|------|--------|------|--------|----------|------|
| fk_pets_owner | users | id | pets | owner_id | CASCADE | 用户删除时，级联删除其宠物 |
| fk_orders_user | users | id | orders | user_id | CASCADE | 用户删除时，级联删除其订单 |
| fk_orders_pet | pets | id | orders | pet_id | CASCADE | 宠物删除时，级联删除其订单 |
| fk_orders_service | services | id | orders | service_id | RESTRICT | 服务被订单引用时，不能删除 |
| fk_orders_staff | users | id | orders | staff_id | SET NULL | 员工删除时，订单的staff_id置空 |
| fk_boardings_order | orders | id | boardings | order_id | CASCADE | 订单删除时，级联删除其寄养记录 |
| fk_boardings_pet | pets | id | boardings | pet_id | CASCADE | 宠物删除时，级联删除其寄养记录 |
| fk_boardings_staff | users | id | boardings | staff_id | CASCADE | 员工删除时，级联删除其寄养记录 |
| fk_health_pet | pets | id | health_records | pet_id | CASCADE | 宠物删除时，级联删除其健康记录 |
| fk_health_vet | users | id | health_records | vet_id | CASCADE | 兽医删除时，级联删除其健康记录 |

## 四、数据库优化设计

### 4.1 索引优化策略

1. **主键索引**：所有表都有自增主键，保证数据唯一性和查询效率
2. **唯一索引**：username、order_no 等关键字段使用唯一索引，保证数据唯一性
3. **外键索引**：所有外键字段都创建索引，加速表连接查询
4. **查询索引**：在常用查询条件字段（status、category、species等）创建索引
5. **复合索引**：在需要多字段组合查询的场景使用复合索引（如寄养表的start_date和end_date）

### 4.2 数据规范化

1. **消除数据冗余**：通过外键关联实现数据引用，避免数据重复
2. **第三范式**：每个字段只依赖于主键，消除传递依赖
3. **数据一致性**：通过外键约束和枚举类型保证数据一致性

### 4.3 性能优化

1. **软删除**：使用 `is_deleted` 标记实现数据的安全删除
2. **时间戳**：自动记录创建和更新时间，便于数据追踪
3. **字段类型优化**：根据实际需求选择合适的字段类型，节省存储空间
4. **CHAR vs VARCHAR**：可变长度字段使用VARCHAR，固定长度字段使用CHAR

## 五、数据完整性保证

### 5.1 实体完整性
- 所有表都有主键，确保每一行数据唯一标识
- 使用 AUTO_INCREMENT 保证主键自动生成

### 5.2 参照完整性
- 通过外键约束保证表间数据的一致性
- 级联删除、SET NULL 等策略保证数据的完整性

### 5.3 用户定义完整性
- 使用 NOT NULL 约束保证关键字段不为空
- 使用 ENUM 类型保证字段的取值范围
- 使用 UNIQUE 约束保证字段的唯一性
- 使用 DEFAULT 值提供默认数据

## 六、扩展性设计

1. **预留字段**：health_status、special_notes 等字段使用 TEXT 类型，便于存储扩展信息
2. **模块化设计**：将不同业务功能拆分为独立表，便于后续扩展
3. **版本控制**：通过 created_at 和 updated_at 字段支持数据版本追踪
