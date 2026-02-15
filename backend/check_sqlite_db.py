import sqlite3
import os

# 连接到SQLite数据库
db_path = os.path.join(os.path.dirname(__file__), 'projectmanagement.db')
try:
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    print(f"成功连接到SQLite数据库: {db_path}")
    
    # 查看数据库中的表
    print("\n数据库中的表:")
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    for table in tables:
        print(f"- {table[0]}")
    
    # 查看每个表的结构
    for table in tables:
        table_name = table[0]
        print(f"\n{table_name}表的结构:")
        cursor.execute(f"PRAGMA table_info({table_name});")
        columns = cursor.fetchall()
        for column in columns:
            print(f"  - {column[1]} ({column[2]})")
    
    # 查看用户表中的数据
    print("\n用户表中的数据:")
    cursor.execute("SELECT id, username FROM users")
    users = cursor.fetchall()
    for user in users:
        print(f"  - {user[1]} (ID: {user[0]})")
    
    # 查看项目表中的数据
    print("\n项目表中的数据:")
    cursor.execute("SELECT id, name, is_deleted FROM projects LIMIT 5")
    projects = cursor.fetchall()
    for project in projects:
        print(f"  - {project[1]} (ID: {project[0]}, is_deleted: {project[2]})")
    
    # 查看待办事项表中的数据
    print("\n待办事项表中的数据:")
    cursor.execute("SELECT id, item FROM todos")
    todos = cursor.fetchall()
    for todo in todos:
        print(f"  - {todo[1]} (ID: {todo[0]})")
    
    conn.close()
    print("\n数据库检查完成")
except Exception as e:
    print(f"检查数据库时出错: {e}")
