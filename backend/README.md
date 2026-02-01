# 宠物管理系统后端

## 📋 项目概述

宠物管理系统后端，基于 FastAPI + MySQL + SQLAlchemy 实现，作为数据库课程设计的后端部分，完整展示数据库设计、ORM 操作、RESTful API 开发等核心技术。

## 🏗️ 技术栈

- **后端框架**: FastAPI 0.104.1
- **数据库**: MySQL 8.0
- **ORM框架**: SQLAlchemy 2.0.23
- **数据验证**: Pydantic 2.5.0
- **认证**: JWT (python-jose)
- **密码加密**: bcrypt (passlib)
- **服务器**: Uvicorn 0.24.0
- **Python版本**: 3.9+

## 📁 项目结构

```
backend/
├── app/
│   ├── api/                    # API路由层
│   │   ├── __init__.py        # 路由注册
│   │   ├── auth.py            # 认证接口
│   │   ├── users.py           # 用户管理
│   │   ├── pets.py            # 宠物档案
│   │   ├── services.py        # 服务管理
│   │   ├── orders.py          # 订单管理
│   │   ├── boardings.py       # 寄养管理
│   │   ├── health_records.py  # 健康记录
│   │   └── dashboard.py       # 仪表盘
│   ├── core/                   # 核心配置层
│   │   ├── __init__.py
│   │   ├── config.py          # 配置管理
│   │   ├── database.py        # 数据库连接
│   │   ├── security.py        # JWT和密码加密
│   │   ├── deps.py            # 依赖注入
│   │   ├── exceptions.py      # 异常处理
│   │   └── response.py        # 统一响应格式
│   ├── crud/                   # 数据访问层
│   │   └── __init__.py        # CRUD操作
│   ├── db/                     # 数据库模型层
│   │   ├── __init__.py
│   │   └── models.py          # SQLAlchemy模型
│   ├── schemas/                # 数据模型层
│   │   └── __init__.py        # Pydantic模型
│   ├── service/                # 业务逻辑层
│   │   └── __init__.py        # 业务逻辑
│   └── main.py                 # 应用入口
├── requirements.txt            # 依赖文件
└── .env                        # 环境变量
```

## 🚀 快速开始

### 1. 环境准备

#### 1.1 安装Python依赖

```bash
cd backend
pip install -r requirements.txt
```

#### 1.2 配置MySQL数据库

1. 安装 MySQL 8.0
2. 创建数据库并执行初始化脚本：

```bash
mysql -u root -p < ../database/init.sql
```

#### 1.3 配置环境变量

编辑 `.env` 文件，配置数据库连接信息：

```env
DATABASE_URL=mysql+pymysql://root:your_password@localhost:3306/pet_management
SECRET_KEY=your-secret-key-here-change-in-production-min-32-chars
```

### 2. 启动服务

```bash
# 开发模式启动
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# 或者使用 uvicorn 命令
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 3. 访问API文档

启动服务后，访问以下地址：

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 📊 数据库设计

### 表结构

1. **users**: 用户表（管理员、宠物主人、员工）
2. **pets**: 宠物档案表
3. **services**: 宠物服务表
4. **orders**: 订单表
5. **boardings**: 寄养表
6. **health_records**: 健康记录表

详细的表结构设计请参考 `../database/DESIGN.md`

## 🔌 核心API接口

### 认证接口

#### 1. 用户登录

**请求示例：**

```bash
curl -X POST "http://localhost:8000/api/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "admin",
    "password": "admin123"
  }'
```

**响应示例：**

```json
{
  "code": 200,
  "msg": "success",
  "data": {
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "token_type": "bearer",
    "user": {
      "id": 1,
      "username": "admin",
      "email": "admin@pet.com",
      "real_name": "系统管理员",
      "role": "admin",
      "is_active": true,
      "created_at": "2025-01-01T00:00:00",
      "updated_at": "2025-01-01T00:00:00"
    }
  }
}
```

#### 2. 获取当前用户信息

**请求示例：**

```bash
curl -X GET "http://localhost:8000/api/auth/me" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

### 仪表盘接口

#### 获取统计数据

**请求示例：**

```bash
curl -X GET "http://localhost:8000/api/dashboard/stats" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

**响应示例：**

```json
{
  "code": 200,
  "msg": "success",
  "data": {
    "total_users": 10,
    "total_pets": 25,
    "total_orders": 50,
    "total_revenue": 15800.00,
    "active_orders": 5
  }
}
```

### 用户管理接口

#### 1. 获取用户列表

**请求示例：**

```bash
curl -X GET "http://localhost:8000/api/users?page=1&size=10" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

**响应示例：**

```json
{
  "code": 200,
  "msg": "success",
  "data": {
    "items": [
      {
        "id": 1,
        "username": "admin",
        "email": "admin@pet.com",
        "real_name": "系统管理员",
        "role": "admin",
        "is_active": true,
        "created_at": "2025-01-01T00:00:00"
      }
    ],
    "total": 10,
    "page": 1,
    "size": 10
  }
}
```

#### 2. 创建用户

**请求示例：**

```bash
curl -X POST "http://localhost:8000/api/users" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "newuser",
    "password": "password123",
    "email": "newuser@example.com",
    "real_name": "新用户",
    "role": "owner"
  }'
```

### 宠物管理接口

#### 1. 获取宠物列表

**请求示例：**

```bash
curl -X GET "http://localhost:8000/api/pets?page=1&size=10" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

**响应示例：**

```json
{
  "code": 200,
  "msg": "success",
  "data": {
    "items": [
      {
        "id": 1,
        "owner_id": 2,
        "name": "小白",
        "species": "猫",
        "breed": "英短",
        "gender": "female",
        "weight": 4.5,
        "color": "白色",
        "created_at": "2025-01-01T00:00:00"
      }
    ],
    "total": 25,
    "page": 1,
    "size": 10
  }
}
```

#### 2. 创建宠物

**请求示例：**

```bash
curl -X POST "http://localhost:8000/api/pets" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "小黑",
    "species": "猫",
    "breed": "美短",
    "gender": "male",
    "birth_date": "2023-03-10",
    "weight": 5.2,
    "color": "黑色"
  }'
```

### 订单管理接口

#### 1. 获取订单列表

**请求示例：**

```bash
curl -X GET "http://localhost:8000/api/orders?page=1&size=10&status=confirmed" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

**响应示例：**

```json
{
  "code": 200,
  "msg": "success",
  "data": {
    "items": [
      {
        "id": 1,
        "order_no": "ORD2025010110001",
        "user_id": 2,
        "pet_id": 1,
        "service_id": 1,
        "staff_id": 3,
        "appointment_time": "2025-02-05T14:00:00",
        "status": "confirmed",
        "total_amount": 88.00,
        "created_at": "2025-01-01T00:00:00"
      }
    ],
    "total": 50,
    "page": 1,
    "size": 10
  }
}
```

#### 2. 创建订单

**请求示例：**

```bash
curl -X POST "http://localhost:8000/api/orders" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "pet_id": 1,
    "service_id": 1,
    "appointment_time": "2025-02-10T14:00:00",
    "notes": "首次服务，请多照顾"
  }'
```

## 🎯 功能特性

### 1. 分层架构设计

- **API路由层**: 处理HTTP请求和响应
- **业务逻辑层**: 实现业务逻辑
- **数据访问层 (CRUD)**: 封装数据库操作
- **数据库模型层 (ORM)**: 定义数据库表结构
- **数据模型层 (Pydantic)**: 数据验证和序列化

### 2. 认证与授权

- **JWT Token认证**: 基于JWT的无状态认证
- **角色权限控制**: 管理员、员工、宠物主人三级权限
- **依赖注入**: 使用FastAPI的依赖注入系统实现权限检查

### 3. 统一响应格式

所有接口返回统一的JSON格式：

```json
{
  "code": 200,
  "msg": "success",
  "data": {}
}
```

### 4. 异常处理

- 全局异常处理器
- 业务异常、数据库异常、通用异常分类处理
- 友好的错误提示

### 5. 数据库操作

- 完整的CRUD操作
- 软删除支持
- 事务管理
- 外键关联

### 6. 分页查询

所有列表接口都支持分页：

- `page`: 页码，从1开始
- `size`: 每页记录数

## 📝 数据库课程设计要点

### 1. 第三范式设计

- 所有表都符合第三范式
- 消除数据冗余
- 保证数据一致性

### 2. 外键关联

- 正确设计外键关系
- 级联删除、SET NULL等策略
- 保证数据完整性

### 3. 索引优化

- 主键索引
- 唯一索引
- 普通索引
- 复合索引

### 4. 数据完整性

- 实体完整性（主键）
- 参照完整性（外键）
- 用户定义完整性（约束）

## 🧪 测试方法

### 1. 使用Swagger UI测试

1. 启动服务
2. 访问 http://localhost:8000/docs
3. 在Swagger UI中直接测试接口

### 2. 使用curl命令测试

参考上面的接口示例

### 3. 使用Postman测试

1. 导入API文档
2. 配置环境变量
3. 执行测试用例

## 📚 默认测试账号

系统初始化时会创建以下测试账号：

| 用户名 | 密码 | 角色 | 说明 |
|--------|------|------|------|
| admin | admin123 | admin | 管理员 |
| owner001 | admin123 | owner | 宠物主人 |
| staff001 | admin123 | staff | 员工 |

## 🔧 开发说明

### 代码规范

- 遵循 PEP 8 编码规范
- 使用类型注解
- 完善的文档字符串
- 详细的代码注释

### Git提交规范

```
feat: 新功能
fix: 修复bug
docs: 文档更新
style: 代码格式调整
refactor: 重构
test: 测试相关
chore: 构建/工具相关
```

## 📖 扩展阅读

- [FastAPI官方文档](https://fastapi.tiangolo.com/)
- [SQLAlchemy官方文档](https://www.sqlalchemy.org/)
- [Pydantic官方文档](https://docs.pydantic.dev/)
- [MySQL官方文档](https://dev.mysql.com/doc/)

## 👨‍💻 作者

宠物管理系统 - 数据库课程设计

## 📄 许可证

MIT License
