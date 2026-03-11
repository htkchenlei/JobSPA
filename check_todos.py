import sqlite3

# 连接到数据库
conn = sqlite3.connect('backend/projectmanagement.db')
cursor = conn.cursor()

# 查看todos表的结构
print("todos表的结构:")
cursor.execute('PRAGMA table_info(todos)')
columns = cursor.fetchall()
for column in columns:
    print(f"  - {column[1]} ({column[2]})")

# 查看todos表中的数据
print("\ntodos表中的数据:")
cursor.execute('SELECT * FROM todos')
todos = cursor.fetchall()
if todos:
    for todo in todos:
        print(f"  - ID: {todo[0]}, Item: {todo[1]}, Is Finished: {todo[3]}, Created By: {todo[5]}")
else:
    print("  无数据")

# 查看users表中的数据，了解用户信息
print("\nusers表中的数据:")
cursor.execute('SELECT id, username FROM users')
users = cursor.fetchall()
for user in users:
    print(f"  - ID: {user[0]}, Username: {user[1]}")

# 关闭连接
conn.close()
