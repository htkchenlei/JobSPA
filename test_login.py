import requests
import json

# 测试登录
url = 'http://localhost:5000/api/auth/login'
headers = {'Content-Type': 'application/json'}

# 尝试使用用户3的凭据登录
data = {
    'username': 'Marco',
    'password': 'password123'
}

response = requests.post(url, headers=headers, json=data)
print(f"Login status code: {response.status_code}")
try:
    print(f"Login response: {response.json()}")
except:
    print(f"Login response: {response.text}")

# 如果登录成功，测试待办事项API
if response.status_code == 200:
    token = response.json().get('token')
    print(f"\nToken: {token}")
    
    # 测试待办事项API
    todo_url = 'http://localhost:5000/api/todos/'
    todo_headers = {
        'Authorization': f'Bearer {token}'
    }
    todo_response = requests.get(todo_url, headers=todo_headers)
    print(f"\nTodo API status code: {todo_response.status_code}")
    print(f"Todo API response: {todo_response.json()}")
    
    # 测试文件管理API
    file_url = 'http://localhost:5000/api/files/'
    file_headers = {
        'Authorization': f'Bearer {token}'
    }
    file_response = requests.get(file_url, headers=file_headers)
    print(f"\nFile API status code: {file_response.status_code}")
    print(f"File API response: {file_response.json()}")
