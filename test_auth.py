import requests
import json

# 测试服务器地址
BASE_URL = 'http://localhost:5000/api'

# 测试用户登录
def test_login():
    print("=== 测试用户登录 ===")
    login_data = {
        "username": "Marco",
        "password": "tianyu.123"
    }
    response = requests.post(f'{BASE_URL}/auth/login', json=login_data)
    print(f"登录状态码: {response.status_code}")
    print(f"登录响应: {response.json()}")
    return response.json().get('token') if response.status_code == 200 else None

# 测试无token访问
def test_no_token_access():
    print("\n=== 测试无token访问 ===")
    # 测试获取todo列表
    response = requests.get(f'{BASE_URL}/todos/')
    print(f"获取todo列表(无token)状态码: {response.status_code}")
    print(f"获取todo列表(无token)响应: {response.json()}")
    
    # 测试获取文件系统
    response = requests.get(f'{BASE_URL}/files/')
    print(f"获取文件系统(无token)状态码: {response.status_code}")
    print(f"获取文件系统(无token)响应: {response.json()}")

# 测试无效token访问
def test_invalid_token_access():
    print("\n=== 测试无效token访问 ===")
    headers = {
        "Authorization": "Bearer invalid_token"
    }
    # 测试获取todo列表
    response = requests.get(f'{BASE_URL}/todos/', headers=headers)
    print(f"获取todo列表(无效token)状态码: {response.status_code}")
    print(f"获取todo列表(无效token)响应: {response.json()}")
    
    # 测试获取文件系统
    response = requests.get(f'{BASE_URL}/files/', headers=headers)
    print(f"获取文件系统(无效token)状态码: {response.status_code}")
    print(f"获取文件系统(无效token)响应: {response.json()}")

# 测试有效token访问
def test_valid_token_access(token):
    print("\n=== 测试有效token访问 ===")
    headers = {
        "Authorization": f"Bearer {token}"
    }
    # 测试获取todo列表
    response = requests.get(f'{BASE_URL}/todos/', headers=headers)
    print(f"获取todo列表(有效token)状态码: {response.status_code}")
    print(f"获取todo列表(有效token)响应: {response.json()}")
    
    # 测试获取文件系统
    response = requests.get(f'{BASE_URL}/files/', headers=headers)
    print(f"获取文件系统(有效token)状态码: {response.status_code}")
    print(f"获取文件系统(有效token)响应: {response.json()}")

if __name__ == "__main__":
    # 测试无token访问
    test_no_token_access()
    
    # 测试无效token访问
    test_invalid_token_access()
    
    # 测试有效token访问
    token = test_login()
    if token:
        test_valid_token_access(token)
    else:
        print("\n登录失败，无法测试有效token访问")
