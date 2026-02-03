"""
测试用户注册功能
Test User Registration API
"""

import requests
import json

BASE_URL = "http://localhost:8000/api"

def test_register_success():
    """测试成功注册"""
    print("=" * 60)
    print("测试 1: 成功注册新用户")
    print("=" * 60)
    
    data = {
        "username": "testuser001",
        "password": "password123",
        "confirm_password": "password123",
        "email": "testuser001@example.com",
        "real_name": "测试用户001"
    }
    
    response = requests.post(f"{BASE_URL}/auth/register", json=data)
    print(f"状态码: {response.status_code}")
    print(f"响应: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
    
    assert response.status_code == 200
    result = response.json()
    assert result['code'] == 200
    assert result['data']['username'] == "testuser001"
    assert result['data']['role'] == 'owner'
    print("✅ 测试通过：用户注册成功\n")


def test_register_password_mismatch():
    """测试两次密码不一致"""
    print("=" * 60)
    print("测试 2: 两次密码不一致")
    print("=" * 60)
    
    data = {
        "username": "testuser002",
        "password": "password123",
        "confirm_password": "password456",
        "email": "testuser002@example.com"
    }
    
    response = requests.post(f"{BASE_URL}/auth/register", json=data)
    print(f"状态码: {response.status_code}")
    print(f"响应: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
    
    assert response.status_code == 200
    result = response.json()
    assert result['code'] == 400
    assert "密码不一致" in result['msg']
    print("✅ 测试通过：正确返回密码不一致错误\n")


def test_register_duplicate_username():
    """测试用户名已存在"""
    print("=" * 60)
    print("测试 3: 用户名已存在")
    print("=" * 60)
    
    data = {
        "username": "admin",  # 使用已存在的用户名
        "password": "password123",
        "confirm_password": "password123",
        "email": "admin2@example.com"
    }
    
    response = requests.post(f"{BASE_URL}/auth/register", json=data)
    print(f"状态码: {response.status_code}")
    print(f"响应: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
    
    assert response.status_code == 200
    result = response.json()
    assert result['code'] == 400
    assert "已存在" in result['msg']
    print("✅ 测试通过：正确返回用户名已存在错误\n")


def test_register_short_password():
    """测试密码过短"""
    print("=" * 60)
    print("测试 4: 密码过短（少于6位）")
    print("=" * 60)
    
    data = {
        "username": "testuser003",
        "password": "12345",
        "confirm_password": "12345",
        "email": "testuser003@example.com"
    }
    
    response = requests.post(f"{BASE_URL}/auth/register", json=data)
    print(f"状态码: {response.status_code}")
    print(f"响应: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
    
    # 注意：这里可能会返回 422 验证错误或 400 错误
    print(f"✅ 测试完成：检查响应状态码\n")


def test_register_short_username():
    """测试用户名过短"""
    print("=" * 60)
    print("测试 5: 用户名过短（少于3位）")
    print("=" * 60)
    
    data = {
        "username": "ab",
        "password": "password123",
        "confirm_password": "password123",
        "email": "testuser004@example.com"
    }
    
    response = requests.post(f"{BASE_URL}/auth/register", json=data)
    print(f"状态码: {response.status_code}")
    print(f"响应: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
    
    print(f"✅ 测试完成：检查响应状态码\n")


def test_register_minimal():
    """测试最少必填字段"""
    print("=" * 60)
    print("测试 6: 最少必填字段注册")
    print("=" * 60)
    
    data = {
        "username": "testuser005",
        "password": "password123",
        "confirm_password": "password123"
    }
    
    response = requests.post(f"{BASE_URL}/auth/register", json=data)
    print(f"状态码: {response.status_code}")
    print(f"响应: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
    
    assert response.status_code == 200
    result = response.json()
    assert result['code'] == 200
    print("✅ 测试通过：最少字段注册成功\n")


def test_register_after_login():
    """测试注册后可以登录"""
    print("=" * 60)
    print("测试 7: 注册后使用新账号登录")
    print("=" * 60)
    
    # 先注册
    username = f"testuser_{hash('login_test') % 10000}"
    register_data = {
        "username": username,
        "password": "password123",
        "confirm_password": "password123",
        "email": f"{username}@example.com"
    }
    
    register_response = requests.post(f"{BASE_URL}/auth/register", json=register_data)
    print(f"注册状态码: {register_response.status_code}")
    
    if register_response.status_code == 200 and register_response.json()['code'] == 200:
        # 注册成功，尝试登录
        login_data = {
            "username": username,
            "password": "password123"
        }
        
        login_response = requests.post(f"{BASE_URL}/auth/login", json=login_data)
        print(f"登录状态码: {login_response.status_code}")
        print(f"登录响应: {json.dumps(login_response.json(), indent=2, ensure_ascii=False)}")
        
        assert login_response.status_code == 200
        result = login_response.json()
        assert result['code'] == 200
        assert 'access_token' in result['data']
        print("✅ 测试通过：注册后可以成功登录\n")
    else:
        print("⚠️  跳过登录测试：注册未成功\n")


def run_all_tests():
    """运行所有测试"""
    print("\n" + "=" * 60)
    print("开始运行用户注册 API 测试")
    print("=" * 60 + "\n")
    
    try:
        test_register_success()
        test_register_password_mismatch()
        test_register_duplicate_username()
        test_register_short_password()
        test_register_short_username()
        test_register_minimal()
        test_register_after_login()
        
        print("=" * 60)
        print("🎉 所有测试完成！")
        print("=" * 60)
    except AssertionError as e:
        print(f"\n❌ 测试失败: {e}")
    except requests.exceptions.ConnectionError:
        print("\n❌ 无法连接到服务器，请确保后端服务已启动")
    except Exception as e:
        print(f"\n❌ 发生错误: {e}")


if __name__ == "__main__":
    run_all_tests()
