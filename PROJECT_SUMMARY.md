# 宠物管理系统 - 数据库课程设计完整项目总结

## 📋 项目概述

本项目是一个完整的宠物管理系统后端，作为数据库课程设计的一部分，充分展示了数据库设计、ORM操作、RESTful API开发等核心技术。系统实现了用户管理、宠物档案、服务管理、订单管理、寄养管理和健康记录等完整功能模块。

### 项目特点

- ✅ **完整的数据库设计**: 6张表，符合第三范式，包含外键关联和索引优化
- ✅ **分层架构设计**: API层、Service层、CRUD层、Model层，职责清晰
- ✅ **JWT认证授权**: 基于Token的无状态认证，支持角色权限控制
- ✅ **RESTful API**: 遵循REST设计规范，统一响应格式
- ✅ **完整CRUD操作**: 所有核心表都实现了增删改查功能
- ✅ **详细代码注释**: 所有代码都包含详细的中文注释
- ✅ **可直接运行**: 提供完整的依赖和配置，开箱即用

## 🏗️ 技术架构

### 技术栈

| 技术 | 版本 | 说明 |
|------|------|------|
| Python | 3.9+ | 编程语言 |
| FastAPI | 0.104.1 | Web框架 |
| MySQL | 8.0 | 数据库 |
| SQLAlchemy | 2.0.23 | ORM框架 |
| Pydantic | 2.5.0 | 数据验证 |
| JWT | python-jose | 认证 |
| bcrypt | passlib | 密码加密 |
| Uvicorn | 0.24.0 | ASGI服务器 |

### 分层架构

```
┌─────────────────────────────────────┐
│       API路由层 (app/api)          │  ← 处理HTTP请求/响应
├─────────────────────────────────────┤
│      业务逻辑层 (app/service)      │  ← 实现业务逻辑
├─────────────────────────────────────┤
│      数据访问层 (app/crud)         │  ← 封装数据库操作
├─────────────────────────────────────┤
│    数据模型层 (app/schemas)        │  ← Pydantic数据验证
├─────────────────────────────────────┤
│    数据库模型层 (app/db/models)    │  ← SQLAlchemy ORM
├─────────────────────────────────────┤
│      核心配置层 (app/core)         │  ← 配置、安全、异常
└─────────────────────────────────────┘
```

## 📊 数据库设计

### 表结构

| 表名 | 说明 | 主要字段 |
|------|------|----------|
| users | 用户表 | id, username, password, role |
| pets | 宠物档案表 | id, owner_id, name, species, gender |
| services | 服务表 | id, name, category, price, is_available |
| orders | 订单表 | id, order_no, user_id, pet_id, service_id, status |
| boardings | 寄养表 | id, order_id, pet_id, staff_id, start_date, end_date |
| health_records | 健康记录表 | id, pet_id, vet_id, type, diagnosis |

### 表关系图

```
users (用户表)
├── 1:N → pets (宠物档案)
├── 1:N → orders (订单，作为发起者)
├── 1:N → orders (订单，作为服务者)
├── 1:N → boardings (寄养)
└── 1:N → health_records (健康记录，作为兽医)

pets (宠物档案)
├── N:1 → users (主人)
├── 1:N → orders
├── 1:N → boardings
└── 1:N → health_records

services (服务表)
└── 1:N → orders

orders (订单表)
├── N:1 → users (发起者)
├── N:1 → pets
├── N:1 → services
├── N:1 → users (服务者)
└── 1:N → boardings
```

### 索引设计

- **主键索引**: 所有表的主键
- **唯一索引**: username, order_no
- **外键索引**: 所有外键字段
- **查询索引**: status, category, species等常用查询字段

## 🔌 API接口总览

### 认证模块 (/api/auth)

| 方法 | 路径 | 说明 | 权限 |
|------|------|------|------|
| POST | /login | 用户登录 | 公开 |
| GET | /me | 获取当前用户信息 | 需登录 |

### 用户管理 (/api/users)

| 方法 | 路径 | 说明 | 权限 |
|------|------|------|------|
| GET | /users | 获取用户列表 | 管理员 |
| GET | /users/{id} | 获取用户详情 | 管理员/本人 |
| POST | /users | 创建用户 | 管理员 |
| PUT | /users/{id} | 更新用户 | 管理员/本人 |
| DELETE | /users/{id} | 删除用户 | 管理员 |

### 宠物档案 (/api/pets)

| 方法 | 路径 | 说明 | 权限 |
|------|------|------|------|
| GET | /pets | 获取宠物列表 | 需登录 |
| GET | /pets/{id} | 获取宠物详情 | 需登录 |
| POST | /pets | 创建宠物 | 需登录 |
| PUT | /pets/{id} | 更新宠物 | 需登录 |
| DELETE | /pets/{id} | 删除宠物 | 需登录 |

### 服务管理 (/api/services)

| 方法 | 路径 | 说明 | 权限 |
|------|------|------|------|
| GET | /services | 获取服务列表 | 需登录 |
| GET | /services/{id} | 获取服务详情 | 需登录 |
| POST | /services | 创建服务 | 员工/管理员 |
| PUT | /services/{id} | 更新服务 | 员工/管理员 |
| DELETE | /services/{id} | 删除服务 | 员工/管理员 |

### 订单管理 (/api/orders)

| 方法 | 路径 | 说明 | 权限 |
|------|------|------|------|
| GET | /orders | 获取订单列表 | 需登录 |
| GET | /orders/{id} | 获取订单详情 | 需登录 |
| POST | /orders | 创建订单 | 需登录 |
| PUT | /orders/{id} | 更新订单 | 需登录 |
| DELETE | /orders/{id} | 删除订单 | 需登录 |

### 寄养管理 (/api/boardings)

| 方法 | 路径 | 说明 | 权限 |
|------|------|------|------|
| GET | /boardings | 获取寄养列表 | 需登录 |
| GET | /boardings/{id} | 获取寄养详情 | 需登录 |
| POST | /boardings | 创建寄养 | 员工/管理员 |
| PUT | /boardings/{id} | 更新寄养 | 员工/管理员 |
| DELETE | /boardings/{id} | 删除寄养 | 员工/管理员 |

### 健康记录 (/api/health-records)

| 方法 | 路径 | 说明 | 权限 |
|------|------|------|------|
| GET | /health-records | 获取健康记录列表 | 需登录 |
| GET | /health-records/{id} | 获取健康记录详情 | 需登录 |
| POST | /health-records | 创建健康记录 | 员工/管理员 |
| PUT | /health-records/{id} | 更新健康记录 | 员工/管理员 |
| DELETE | /health-records/{id} | 删除健康记录 | 员工/管理员 |

### 仪表盘 (/api/dashboard)

| 方法 | 路径 | 说明 | 权限 |
|------|------|------|------|
| GET | /stats | 获取统计数据 | 员工/管理员 |

## 🚀 快速开始

### 1. 环境准备

```bash
# 1. 安装Python依赖
cd backend
pip install -r requirements.txt

# 2. 初始化数据库
mysql -u root -p < ../database/init.sql

# 3. 配置环境变量
# 编辑 backend/.env 文件，修改数据库连接信息
```

### 2. 启动服务

```bash
# 开发模式启动
python -m uvicorn app.main:app --reload

# 访问API文档
# http://localhost:8000/docs
```

### 3. 测试接口

```bash
# 登录获取Token
curl -X POST "http://localhost:8000/api/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "admin123"}'

# 使用Token访问受保护的接口
curl -X GET "http://localhost:8000/api/dashboard/stats" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

## 📦 项目结构

```
Pet_management/
├── database/                   # 数据库相关
│   ├── init.sql              # 建表SQL
│   └── DESIGN.md             # 数据库设计文档
│
├── backend/                    # 后端项目
│   ├── app/
│   │   ├── api/              # API路由层
│   │   │   ├── __init__.py
│   │   │   ├── auth.py      # 认证接口
│   │   │   ├── users.py     # 用户管理
│   │   │   ├── pets.py      # 宠物档案
│   │   │   ├── services.py  # 服务管理
│   │   │   ├── orders.py    # 订单管理
│   │   │   ├── boardings.py # 寄养管理
│   │   │   ├── health_records.py # 健康记录
│   │   │   └── dashboard.py # 仪表盘
│   │   ├── core/             # 核心配置层
│   │   │   ├── config.py    # 配置管理
│   │   │   ├── database.py  # 数据库连接
│   │   │   ├── security.py  # JWT和安全
│   │   │   ├── deps.py      # 依赖注入
│   │   │   ├── exceptions.py# 异常处理
│   │   │   └── response.py  # 统一响应
│   │   ├── crud/             # 数据访问层
│   │   │   └── __init__.py  # CRUD操作
│   │   ├── db/               # 数据库模型层
│   │   │   ├── __init__.py
│   │   │   └── models.py    # SQLAlchemy模型
│   │   ├── schemas/          # 数据模型层
│   │   │   └── __init__.py  # Pydantic模型
│   │   ├── service/          # 业务逻辑层
│   │   │   └── __init__.py  # 业务逻辑
│   │   └── main.py           # 应用入口
│   ├── requirements.txt       # 依赖文件
│   ├── .env                  # 环境变量
│   └── README.md             # 后端说明文档
│
└── PROJECT_SUMMARY.md        # 项目总结（本文件）
```

## 🎯 数据库课程设计要点

### 1. 第三范式设计

- ✅ 所有表都符合第三范式要求
- ✅ 消除了非主属性对码的传递依赖
- ✅ 保证数据的一致性和完整性

### 2. 外键关系设计

- ✅ 正确设计了一对多关系
- ✅ 合理使用了级联删除和SET NULL策略
- ✅ 保证了参照完整性

### 3. 索引优化

- ✅ 主键索引：保证数据唯一性
- ✅ 唯一索引：username、order_no
- ✅ 外键索引：加速表连接查询
- ✅ 查询索引：status、category等字段

### 4. 数据完整性

- ✅ 实体完整性：主键约束
- ✅ 参照完整性：外键约束
- ✅ 用户定义完整性：非空、唯一、默认值、枚举类型

### 5. 数据库操作

- ✅ 完整的CRUD操作
- ✅ 软删除支持
- ✅ 事务管理
- ✅ 复杂查询（统计、筛选、分页）

## 🔐 认证与权限

### JWT认证流程

```
1. 用户登录 → 验证用户名密码 → 生成JWT Token
2. 客户端携带Token访问受保护接口
3. 服务端验证Token有效性 → 提取用户信息 → 执行业务逻辑
```

### 角色权限设计

| 角色 | 权限说明 |
|------|----------|
| admin | 系统管理员，拥有所有权限 |
| staff | 员工，可以查看和操作服务、订单、寄养、健康记录 |
| owner | 宠物主人，只能操作自己的宠物和订单 |

### 依赖注入实现

```python
# 认证依赖
async def get_current_active_user(current_user = Depends(get_current_active_user))

# 角色依赖
require_admin = RoleChecker(["admin"])
require_staff = RoleChecker(["admin", "staff"])
require_owner = RoleChecker(["admin", "staff", "owner"])
```

## 📝 代码规范

### 遵循的规范

- PEP 8 Python编码规范
- 类型注解 (Type Hints)
- 完整的文档字符串 (Docstrings)
- 详细的代码注释
- 统一的命名规范

### 代码分层原则

- **API层**: 只处理HTTP请求和响应，不包含业务逻辑
- **Service层**: 实现业务逻辑，调用CRUD层
- **CRUD层**: 封装数据库操作，不包含业务逻辑
- **Model层**: 定义数据结构，不包含业务逻辑

## 🧪 测试方法

### 1. Swagger UI测试

1. 启动服务后访问 http://localhost:8000/docs
2. 点击接口进行测试
3. 自动生成请求数据和显示响应

### 2. 命令行测试

```bash
# 登录
curl -X POST "http://localhost:8000/api/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "admin123"}'

# 获取统计
curl -X GET "http://localhost:8000/api/dashboard/stats" \
  -H "Authorization: Bearer TOKEN"

# 获取用户列表
curl -X GET "http://localhost:8000/api/users?page=1&size=10" \
  -H "Authorization: Bearer TOKEN"
```

### 3. Postman测试

1. 导入API文档（通过OpenAPI导入）
2. 配置环境变量（Token）
3. 执行测试用例

## 📚 默认测试账号

| 用户名 | 密码 | 角色 | 说明 |
|--------|------|------|------|
| admin | admin123 | admin | 系统管理员 |
| owner001 | admin123 | owner | 宠物主人 |
| staff001 | admin123 | staff | 员工 |

## 📖 课设报告建议

### 报告结构建议

1. **项目概述**
   - 项目背景
   - 技术选型
   - 功能模块

2. **数据库设计**
   - E-R图
   - 表结构设计
   - 关系设计
   - 索引设计

3. **系统设计**
   - 架构设计
   - 模块划分
   - 接口设计

4. **功能实现**
   - 核心功能介绍
   - 关键代码展示
   - 数据库操作展示

5. **系统测试**
   - 接口测试
   - 功能测试
   - 性能测试

6. **总结与展望**
   - 项目总结
   - 存在问题
   - 改进方向

## 🔧 常见问题

### 1. 数据库连接失败

**问题**: `sqlalchemy.exc.OperationalError`

**解决**: 检查 `.env` 文件中的数据库连接配置是否正确

### 2. JWT Token过期

**问题**: 401 Unauthorized

**解决**: 重新登录获取新的Token

### 3. 权限不足

**问题**: 403 Forbidden

**解决**: 检查用户角色是否具有相应权限

## 📞 技术支持

- FastAPI文档: https://fastapi.tiangolo.com/
- SQLAlchemy文档: https://www.sqlalchemy.org/
- Pydantic文档: https://docs.pydantic.dev/
- MySQL文档: https://dev.mysql.com/doc/

## 🎓 学习收获

通过本项目，可以学习到：

1. **数据库设计**: 第三范式、外键关系、索引优化
2. **ORM框架**: SQLAlchemy的使用，表关系映射
3. **Web框架**: FastAPI的使用，依赖注入
4. **认证授权**: JWT实现，权限控制
5. **分层架构**: 如何设计清晰的代码架构
6. **API设计**: RESTful API设计规范
7. **数据验证**: Pydantic数据验证

## 📄 许可证

MIT License

---

**宠物管理系统 - 数据库课程设计**

祝课设顺利！🎉
