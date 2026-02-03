用户要求：
1. 将后端的测试文件单独放一个目录整理
2. 如果有专门的测试框架就使用
3. 写 commit

我需要：
1. 查看项目是否已经有测试框架（pytest 等）
2. 创建测试目录结构
3. 将测试文件移动到测试目录
4. 如果有 pytest，按照 pytest 规范编写测试
5. 提交 commit

让我先查看项目结构和 requirements.txt
看起来项目没有 pytest，我需要：
1. 创建 tests 目录
2. 将 test_register.py 移动到 tests 目录
3. 按照 pytest 规范重构测试代码
4. 添加 pytest 到 requirements.txt
5. 创建 pytest 配置文件
6. 提交 commit
现在我需要：
1. 删除旧的 test_register.py 文件
2. 提交 commit
看起来删除操作失败了（文件不在 workspace 目录），但是其他操作成功了。我需要手动删除 test_register.py 文件。让我先检查一下文件是否还存在。
看起来 test_register.py 文件还在那里，但是没有在 git 中（因为之前已经提交过了）。我需要删除这个文件，然后提交删除操作。让我使用 git rm 命令删除已跟踪的文件。
很好！现在所有的操作都完成了。让我创建一个简单的测试运行指南文档，然后总结一下。
commit 似乎没有成功，让我再试一次。
太好了！所有的 commit 都成功了。现在让我总结一下完成的工作。
完成！已成功整理测试目录结构并使用 pytest 测试框架。

## 📋 提交记录

```
85f010a - test:add_quick_test_runner
285bb59 - chore:remove_old_test_file
cde98c0 - refactor:reorganize_test_structure
478243b - feat:add_user_registration_ui
7ca767c - test:add_user_registration_tests
0172397 - feat:add_user_registration_endpoint
```

---

## 🗂️ 新建测试目录结构

```
backend/
├── tests/
│   ├── __init__.py              # 测试包初始化
│   ├── README.md                # 测试文档
│   └── test_auth_api.py         # 认证 API 测试（使用 pytest）
├── pytest.ini                   # pytest 配置文件
├── run_tests.py                # 快速测试运行脚本
└── requirements.txt            # 已添加 pytest 依赖
```

---

## ✨ 改进内容

### 1. 使用 pytest 测试框架
- ✅ 添加 `pytest` 和相关依赖到 `requirements.txt`
- ✅ 创建 `pytest.ini` 配置文件
- ✅ 按照 pytest 规范重构测试代码

### 2. 测试代码重构 (`tests/test_auth_api.py`)

**使用 pytest 的优势：**
- 📦 测试类结构：`TestRegisterAPI`, `TestLoginAPI`, `TestGetCurrentUserAPI`
- 🏷️ 测试标记：支持 `@pytest.mark.auth`, `@pytest.mark.api` 等
- ⚡ 自动测试发现：无需手动导入
- 📊 丰富的断言和报告

**测试用例：**
```python
class TestRegisterAPI:
    def test_register_success(self)
    def test_register_password_mismatch(self)
    def test_register_duplicate_username(self)
    def test_register_short_password(self)
    def test_register_short_username(self)
    def test_register_minimal_fields(self)
    def test_register_then_login(self)

class TestLoginAPI:
    def test_login_success(self)
    def test_login_wrong_password(self)
    def test_login_nonexistent_user(self)

class TestGetCurrentUserAPI:
    def test_get_current_user_without_token(self)
    def test_get_current_user_with_token(self)
```

### 3. 测试配置 (`pytest.ini`)

```ini
[pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
addopts = -v --strict-markers --tb=short
markers =
    auth: 认证相关测试
    users: 用户相关测试
    # ... 更多标记
```

### 4. 测试文档 (`tests/README.md`)

包含：
- 测试框架说明
- 目录结构
- 安装依赖方法
- 运行测试的各种方式
- 测试标记说明
- 测试编写规范
- 注意事项

### 5. 快速测试脚本 (`run_tests.py`)

```bash
# 运行所有测试
python backend/run_tests.py

# 或直接使用 pytest
cd backend
pytest                    # 运行所有测试
pytest tests/test_auth_api.py              # 运行特定文件
pytest tests/test_auth_api.py::TestRegisterAPI  # 运行特定类
pytest -m auth          # 运行标记的测试
pytest -v               # 详细输出
```

---

## 🚀 使用方式

### 安装依赖
```bash
cd backend
pip install -r requirements.txt
```

### 运行测试

**方式一：使用快速脚本**
```bash
cd backend
python run_tests.py
```

**方式二：使用 pytest 命令**
```bash
cd backend
pytest                          # 运行所有测试
pytest -v                       # 详细输出
pytest -m auth                   # 只运行认证测试
pytest tests/test_auth_api.py    # 运行特定文件
```

**方式三：运行特定测试**
```bash
pytest tests/test_auth_api.py::TestRegisterAPI::test_register_success
```

---

## 📊 测试标记

| 标记 | 说明 |
|------|------|
| `auth` | 认证相关测试 |
| `users` | 用户相关测试 |
| `pets` | 宠物相关测试 |
| `orders` | 订单相关测试 |
| `services` | 服务相关测试 |
| `boardings` | 寄养相关测试 |
| `health_records` | 健康记录相关测试 |
| `api` | API 接口测试 |
| `integration` | 集成测试 |
| `unit` | 单元测试 |

---

## 📝 未来扩展

可以继续在 `tests/` 目录下添加更多测试文件：

- `test_users_api.py` - 用户管理 API 测试
- `test_pets_api.py` - 宠物管理 API 测试
- `test_orders_api.py` - 订单管理 API 测试
- `test_services_api.py` - 服务管理 API 测试
- `test_boardings_api.py` - 寄养管理 API 测试
- `test_health_records.py` - 健康记录 API 测试

---

## ✅ 验证清单

- [x] 创建 `tests/` 目录
- [x] 使用 pytest 测试框架
- [x] 添加 pytest 配置文件
- [x] 添加测试文档
- [x] 创建快速测试运行脚本
- [x] 重构测试代码为 pytest 风格
- [x] 删除旧的测试文件
- [x] 更新 requirements.txt
- [x] 所有代码已提交到 Git

测试结构已整理完成！🎉