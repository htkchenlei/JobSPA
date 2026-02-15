import mysql.connector
import os

# 连接到MySQL数据库
try:
    conn = mysql.connector.connect(
        host='localhost',
        user='root',
        password='root',
        database='projectmanagement'
    )
    cursor = conn.cursor()
    
    # 检查用户表
    print("\nChecking users table:")
    cursor.execute("SELECT id, username FROM users")
    users = cursor.fetchall()
    for user in users:
        print(f"User: {user[1]} (ID: {user[0]})")
    
    # 检查待办事项表
    print("\nChecking todos table:")
    cursor.execute("SELECT id, item, created_by FROM todos")
    todos = cursor.fetchall()
    for todo in todos:
        print(f"Todo: {todo[1]} (ID: {todo[0]}, Created by: {todo[2]})")
    
    # 检查文件管理的根目录
    print("\nChecking file uploads directory:")
    uploads_dir = os.path.join(os.path.dirname(__file__), 'backend', 'uploads')
    print(f"Uploads directory: {uploads_dir}")
    print(f"Directory exists: {os.path.exists(uploads_dir)}")
    
    if os.path.exists(uploads_dir):
        print("\nContents of uploads directory:")
        for item in os.listdir(uploads_dir):
            item_path = os.path.join(uploads_dir, item)
            if os.path.isdir(item_path):
                print(f"Directory: {item}")
                # 检查子目录
                for subitem in os.listdir(item_path):
                    print(f"  - {subitem}")
            else:
                print(f"File: {item}")
    
    cursor.close()
    conn.close()
    
except Exception as e:
    print(f"Error: {e}")
