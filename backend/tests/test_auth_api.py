"""
认证 API 测试
Authentication API Tests
"""

import pytest
import requests
from typing import Dict, Any

BASE_URL = "http://localhost:8000/api"


class TestRegisterAPI:
    """用户注册 API 测试类"""
    
    @staticmethod
    def generate_test_user() -> Dict[str, Any]:
        """生成测试用户数据"""
        import random
        import time
        timestamp = int(time.time() * 1000)
        return {
            "username": f"testuser_{timestamp}_{random.randint(1000, 9999)}",
            "password": "password123",
            "confirm_password": "password123",
            "email": f"testuser_{timestamp}@example.com",
            "real_name": "测试用户"
        }
    
    def test_register_success(self):
        """测试成功注册新用户"""
        data = self.generate_test_user()
        
        response = requests.post(f"{BASE_URL}/auth/register", json=data)
        
        assert response.status_code == 200
        result = response.json()
        assert result['code'] == 200
        assert result['data']['username'] == data['username']
        assert result['data']['role'] == 'owner'
        assert result['data']['is_active'] is True
    
    def test_register_password_mismatch(self):
        """测试两次密码不一致"""
        data = self.generate_test_user()
        data['confirm_password'] = "wrongpassword"
        
        response = requests.post(f"{BASE_URL}/auth/register", json=data)
        
        assert response.status_code == 200
        result = response.json()
        assert result['code'] == 400
        assert '密码' in result['msg'] and '不一致' in result['msg']
    
    def test_register_duplicate_username(self):
        """测试用户名已存在"""
        data = self.generate_test_user()
        data['username'] = 'admin'  # 使用已存在的用户名
        
        response = requests.post(f"{BASE_URL}/auth/register", json=data)
        
        assert response.status_code == 200
        result = response.json()
        assert result['code'] == 400
        assert '已存在' in result['msg']
    
    def test_register_short_password(self):
        """测试密码过短（少于6位）"""
        data = self.generate_test_user()
        data['password'] = '12345'
        data['confirm_password'] = '12345'
        
        response = requests.post(f"{BASE_URL}/auth/register", json=data)
        
        # Pydantic 验证错误返回 422
        assert response.status_code in [400, 422]
    
    def test_register_short_username(self):
        """测试用户名过短（少于3位）"""
        data = self.generate_test_user()
        data['username'] = 'ab'
        
        response = requests.post(f"{BASE_URL}/auth/register", json=data)
        
        # Pydantic 验证错误返回 422
        assert response.status_code in [400, 422]
    
    def test_register_minimal_fields(self):
        """测试最少必填字段注册"""
        data = {
            "username": f"testuser_minimal_{int(__import__('time').time() * 1000)}",
            "password": "password123",
            "confirm_password": "password123"
        }
        
        response = requests.post(f"{BASE_URL}/auth/register", json=data)
        
        assert response.status_code == 200
        result = response.json()
        assert result['code'] == 200
        assert result['data']['username'] == data['username']
    
    def test_register_then_login(self):
        """测试注册后可以登录"""
        # 注册
        register_data = self.generate_test_user()
        register_response = requests.post(f"{BASE_URL}/auth/register", json=register_data)
        
        assert register_response.status_code == 200
        register_result = register_response.json()
        assert register_result['code'] == 200
        
        # 登录
        login_data = {
            "username": register_data['username'],
            "password": register_data['password']
        }
        
        login_response = requests.post(f"{BASE_URL}/auth/login", json=login_data)
        
        assert login_response.status_code == 200
        login_result = login_response.json()
        assert login_result['code'] == 200
        assert 'access_token' in login_result['data']
        assert login_result['data']['user']['username'] == register_data['username']


class TestLoginAPI:
    """用户登录 API 测试类"""
    
    def test_login_success(self):
        """测试成功登录"""
        data = {
            "username": "admin",
            "password": "admin123"
        }
        
        response = requests.post(f"{BASE_URL}/auth/login", json=data)
        
        assert response.status_code == 200
        result = response.json()
        assert result['code'] == 200
        assert 'access_token' in result['data']
        assert 'user' in result['data']
        assert result['data']['user']['username'] == 'admin'
    
    def test_login_wrong_password(self):
        """测试密码错误"""
        data = {
            "username": "admin",
            "password": "wrongpassword"
        }
        
        response = requests.post(f"{BASE_URL}/auth/login", json=data)
        
        assert response.status_code == 200
        result = response.json()
        assert result['code'] == 401
        assert '用户名或密码错误' in result['msg']
    
    def test_login_nonexistent_user(self):
        """测试用户不存在"""
        data = {
            "username": "nonexistentuser999",
            "password": "password123"
        }
        
        response = requests.post(f"{BASE_URL}/auth/login", json=data)
        
        assert response.status_code == 200
        result = response.json()
        assert result['code'] == 401
        assert '用户名或密码错误' in result['msg']


class TestGetCurrentUserAPI:
    """获取当前用户 API 测试类"""
    
    def test_get_current_user_without_token(self):
        """测试未携带 Token 获取用户信息"""
        response = requests.get(f"{BASE_URL}/auth/me")
        
        # 未携带 Token 应该返回 401 或 403
        assert response.status_code in [401, 403]
    
    def test_get_current_user_with_token(self):
        """测试携带 Token 获取用户信息"""
        # 先登录获取 token
        login_data = {
            "username": "admin",
            "password": "admin123"
        }
        login_response = requests.post(f"{BASE_URL}/auth/login", json=login_data)
        token = login_response.json()['data']['access_token']
        
        # 携带 token 获取用户信息
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.get(f"{BASE_URL}/auth/me", headers=headers)
        
        assert response.status_code == 200
        result = response.json()
        assert result['code'] == 200
        assert result['data']['username'] == 'admin'
