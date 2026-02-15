import requests

# 测试后端API是否正常工作
base_url = 'http://localhost:5000/api'

print("测试后端API是否正常工作...")

# 测试获取待办事项
print("\n测试获取待办事项:")
try:
    response = requests.get(f"{base_url}/todos/")
    print(f"状态码: {response.status_code}")
    print(f"响应内容: {response.json()}")
except Exception as e:
    print(f"错误: {e}")

# 测试获取项目列表
print("\n测试获取项目列表:")
try:
    response = requests.get(f"{base_url}/projects/")
    print(f"状态码: {response.status_code}")
    print(f"响应内容: {response.json()}")
except Exception as e:
    print(f"错误: {e}")

# 测试获取用户列表
print("\n测试获取用户列表:")
try:
    response = requests.get(f"{base_url}/users/")
    print(f"状态码: {response.status_code}")
    print(f"响应内容: {response.json()}")
except Exception as e:
    print(f"错误: {e}")
