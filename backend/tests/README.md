# 后端测试文档

## 测试框架

本项目使用 `pytest` 作为测试框架。

## 目录结构

```
tests/
├── __init__.py              # 测试包初始化文件
├── test_auth_api.py         # 认证 API 测试
├── test_users_api.py        # 用户管理 API 测试
├── test_pets_api.py         # 宠物管理 API 测试
├── test_orders_api.py       # 订单管理 API 测试
├── test_services_api.py     # 服务管理 API 测试
├── test_boardings_api.py    # 寄养管理 API 测试
├── test_health_records.py   # 健康记录 API 测试
└── README.md                # 本文档
```

## 安装测试依赖

```bash
pip install -r requirements.txt
```

或单独安装 pytest：

```bash
pip install pytest pytest-asyncio requests
```

## 运行测试

### 运行所有测试

```bash
pytest
```

### 运行特定测试文件

```bash
pytest tests/test_auth_api.py
```

### 运行特定测试类

```bash
pytest tests/test_auth_api.py::TestRegisterAPI
```

### 运行特定测试方法

```bash
pytest tests/test_auth_api.py::TestRegisterAPI::test_register_success
```

### 运行标记的测试

```bash
pytest -m auth      # 只运行认证相关测试
pytest -m api       # 只运行 API 测试
pytest -m unit      # 只运行单元测试
pytest -m integration # 只运行集成测试
```

### 显示详细输出

```bash
pytest -v
```

### 显示打印输出

```bash
pytest -s
```

### 生成覆盖率报告

```bash
pytest --cov=app tests/
```

## 测试标记

- `auth`: 认证相关测试
- `users`: 用户相关测试
- `pets`: 宠物相关测试
- `orders`: 订单相关测试
- `services`: 服务相关测试
- `boardings`: 寄养相关测试
- `health_records`: 健康记录相关测试
- `api`: API 接口测试
- `integration`: 集成测试
- `unit`: 单元测试

## 测试规范

### 命名规范

- 测试文件：`test_*.py` 或 `*_test.py`
- 测试类：`Test*`
- 测试方法：`test_*`

### 编写规范

1. 使用 pytest 断言风格：`assert condition`
2. 使用描述性的测试方法名
3. 每个测试应该独立运行
4. 使用 fixture 进行数据准备和清理
5. 测试失败时提供清晰的错误信息

### 示例

```python
import pytest

class TestUserAPI:
    """用户 API 测试类"""
    
    def test_create_user_success(self):
        """测试成功创建用户"""
        # Given - 准备测试数据
        user_data = {"username": "test", "password": "123456"}
        
        # When - 执行操作
        response = create_user(user_data)
        
        # Then - 验证结果
        assert response.status_code == 200
        assert response.data['username'] == 'test'
    
    @pytest.mark.auth
    def test_create_user_without_auth(self):
        """测试未认证创建用户"""
        pass
```

## 运行前准备

确保后端服务已启动：

```bash
cd backend
python -m uvicorn app.main:app --reload
```

或者在 CI/CD 环境中启动测试数据库和后端服务。

## 持续集成

测试会在 CI/CD 流程中自动运行，确保代码质量。

## 注意事项

1. 测试会创建测试数据，请在测试环境中运行
2. 不要在生产环境运行测试
3. 测试数据库应与开发/生产数据库分离
