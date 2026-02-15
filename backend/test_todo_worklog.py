import requests

# 测试待办事项和工作日志的API路由
base_url = 'http://localhost:5000/api'

print("测试待办事项和工作日志的API路由...")

# 测试获取待办事项列表
print("\n测试获取待办事项列表:")
try:
    # 注意：待办事项API需要授权访问，需要提供token
    # 这里使用一个假的token，应该会返回401未授权错误
    headers = {'Authorization': 'Bearer fake-token'}
    response = requests.get(f"{base_url}/todos/", headers=headers)
    print(f"状态码: {response.status_code}")
    print(f"响应内容: {response.json()}")
except Exception as e:
    print(f"错误: {e}")

# 测试获取工作日志列表
print("\n测试获取工作日志列表:")
try:
    response = requests.get(f"{base_url}/work-log/")
    print(f"状态码: {response.status_code}")
    print(f"响应内容: {response.json()}")
except Exception as e:
    print(f"错误: {e}")

# 测试获取今日活动记录
print("\n测试获取今日活动记录:")
try:
    response = requests.get(f"{base_url}/work-log/today-activities")
    print(f"状态码: {response.status_code}")
    print(f"响应内容: {response.json()}")
except Exception as e:
    print(f"错误: {e}")
