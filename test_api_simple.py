import requests

# 测试待办事项API
print("Testing Todo API...")
todo_response = requests.get('http://localhost:5000/api/todos/')
print(f"Status code: {todo_response.status_code}")
print(f"Response: {todo_response.json()}")

# 测试文件管理API
print("\nTesting File API...")
file_response = requests.get('http://localhost:5000/api/files/')
print(f"Status code: {file_response.status_code}")
print(f"Response: {file_response.json()}")
