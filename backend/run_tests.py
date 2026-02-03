#!/usr/bin/env python
"""
快速测试脚本
Quick Test Script

运行所有测试并显示结果
"""

import subprocess
import sys

def run_tests():
    """运行测试"""
    print("=" * 70)
    print("运行 Pet Management System 测试")
    print("=" * 70)
    print()
    
    # 检查后端服务是否运行
    try:
        import requests
        response = requests.get("http://localhost:8000/health", timeout=2)
        if response.status_code == 200:
            print("✅ 后端服务运行正常")
        else:
            print("⚠️  后端服务状态异常，测试可能会失败")
    except:
        print("❌ 后端服务未运行，请先启动：")
        print("   python -m uvicorn app.main:app --reload")
        sys.exit(1)
    
    print()
    print("=" * 70)
    print("开始运行测试...")
    print("=" * 70)
    print()
    
    # 运行 pytest
    result = subprocess.run(
        [sys.executable, "-m", "pytest", "tests/", "-v", "--tb=short"],
        cwd=".",
        capture_output=False
    )
    
    print()
    print("=" * 70)
    if result.returncode == 0:
        print("🎉 所有测试通过！")
    else:
        print("❌ 测试失败，请检查上面的错误信息")
    print("=" * 70)
    
    return result.returncode

if __name__ == "__main__":
    sys.exit(run_tests())
