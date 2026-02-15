import mysql.connector
import sqlite3
import os
import sys
import datetime

# 添加当前目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# 连接到MySQL数据库
try:
    mysql_conn = mysql.connector.connect(
        host='localhost',
        user='root',
        password='root',
        database='projectmanagement'
    )
    mysql_cursor = mysql_conn.cursor()
    print("成功连接到MySQL数据库")
except Exception as e:
    print(f"连接MySQL数据库失败: {e}")
    sys.exit(1)

# 创建SQLite数据库连接
sqlite_db_path = os.path.join(os.path.dirname(__file__), 'projectmanagement.db')
try:
    sqlite_conn = sqlite3.connect(sqlite_db_path)
    sqlite_cursor = sqlite_conn.cursor()
    print(f"成功创建SQLite数据库: {sqlite_db_path}")
except Exception as e:
    print(f"创建SQLite数据库失败: {e}")
    mysql_cursor.close()
    mysql_conn.close()
    sys.exit(1)

# 创建表结构
print("开始创建表结构...")

# 创建用户表
sqlite_cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL,
    is_admin BOOLEAN NOT NULL DEFAULT 0,
    is_enable BOOLEAN NOT NULL DEFAULT 1
)
''')

# 创建项目表
sqlite_cursor.execute('''
CREATE TABLE IF NOT EXISTS projects (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    client_name TEXT NOT NULL,
    scale TEXT,
    start_date DATE,
    location TEXT,
    sales_person TEXT,
    stage INTEGER NOT NULL DEFAULT 1,
    is_deleted BOOLEAN NOT NULL DEFAULT 0,
    owner INTEGER,
    province TEXT,
    city TEXT,
    district TEXT
)
''')

# 创建项目进展表
sqlite_cursor.execute('''
CREATE TABLE IF NOT EXISTS project_progress (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    project_id INTEGER NOT NULL,
    update_content TEXT NOT NULL,
    update_date DATE NOT NULL,
    updated_by INTEGER NOT NULL,
    update_time TEXT NOT NULL,
    is_important INTEGER NOT NULL DEFAULT 0,
    FOREIGN KEY (project_id) REFERENCES projects (id),
    FOREIGN KEY (updated_by) REFERENCES users (id)
)
''')

# 创建项目最新更新表
sqlite_cursor.execute('''
CREATE TABLE IF NOT EXISTS latest_update (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    project_id INTEGER NOT NULL UNIQUE,
    update_content TEXT NOT NULL,
    update_date DATE NOT NULL,
    updated_by INTEGER NOT NULL,
    update_time TEXT NOT NULL,
    FOREIGN KEY (project_id) REFERENCES projects (id),
    FOREIGN KEY (updated_by) REFERENCES users (id)
)
''')

# 创建待办事项表
sqlite_cursor.execute('''
CREATE TABLE IF NOT EXISTS todos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    item TEXT NOT NULL,
    create_at TIMESTAMP,
    is_finished BOOLEAN DEFAULT 0,
    finish_at TIMESTAMP,
    created_by INTEGER NOT NULL,
    FOREIGN KEY (created_by) REFERENCES users (id)
)
''')

# 创建工作日志表
sqlite_cursor.execute('''
CREATE TABLE IF NOT EXISTS work_log (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    today_activities TEXT,
    user INTEGER NOT NULL,
    work_log_by_ai TEXT,
    log_date DATE,
    log_time TEXT,
    created_by_ai TEXT DEFAULT 'DeepSeek',
    FOREIGN KEY (user) REFERENCES users (id)
)
''')

# 清空表数据
sqlite_cursor.execute('DELETE FROM work_log')
sqlite_cursor.execute('DELETE FROM todos')
sqlite_cursor.execute('DELETE FROM latest_update')
sqlite_cursor.execute('DELETE FROM project_progress')
sqlite_cursor.execute('DELETE FROM projects')
sqlite_cursor.execute('DELETE FROM users')
# 重置自增ID
sqlite_cursor.execute('DELETE FROM sqlite_sequence WHERE name="work_log"')
sqlite_cursor.execute('DELETE FROM sqlite_sequence WHERE name="todos"')
sqlite_cursor.execute('DELETE FROM sqlite_sequence WHERE name="latest_update"')
sqlite_cursor.execute('DELETE FROM sqlite_sequence WHERE name="project_progress"')
sqlite_cursor.execute('DELETE FROM sqlite_sequence WHERE name="projects"')
sqlite_cursor.execute('DELETE FROM sqlite_sequence WHERE name="users"')

sqlite_conn.commit()
print("表结构创建完成")

# 迁移用户数据
print("开始迁移用户数据...")
mysql_cursor.execute("SELECT id, username, password, is_admin, is_enable FROM users")
users = mysql_cursor.fetchall()
for user in users:
    sqlite_cursor.execute('''
    INSERT INTO users (id, username, password, is_admin, is_enable) 
    VALUES (?, ?, ?, ?, ?)
    ''', user)
sqlite_conn.commit()
print(f"迁移了 {len(users)} 个用户")

# 迁移项目数据
print("开始迁移项目数据...")
mysql_cursor.execute('''
SELECT id, name, client_name, scale, start_date, location, sales_person, 
       stage, is_deleted, owner, province, city, district 
FROM projects
''')
projects = mysql_cursor.fetchall()
for project in projects:
    sqlite_cursor.execute('''
    INSERT INTO projects (id, name, client_name, scale, start_date, location, sales_person, 
                         stage, is_deleted, owner, province, city, district) 
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', project)
sqlite_conn.commit()
print(f"迁移了 {len(projects)} 个项目")

# 转换时间类型函数
def convert_time(value):
    if isinstance(value, datetime.timedelta):
        # 转换 timedelta 为 HH:MM:SS 格式
        total_seconds = int(value.total_seconds())
        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60
        seconds = total_seconds % 60
        return f"{hours:02d}:{minutes:02d}:{seconds:02d}"
    return value

# 迁移项目进展数据
print("开始迁移项目进展数据...")
mysql_cursor.execute('''
SELECT id, project_id, update_content, update_date, updated_by, update_time, is_important 
FROM project_progress
''')
project_progresses = mysql_cursor.fetchall()
for progress in project_progresses:
    # 转换时间类型
    progress_data = list(progress)
    progress_data[5] = convert_time(progress_data[5])  # update_time
    sqlite_cursor.execute('''
    INSERT INTO project_progress (id, project_id, update_content, update_date, updated_by, update_time, is_important) 
    VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', progress_data)
sqlite_conn.commit()
print(f"迁移了 {len(project_progresses)} 条项目进展记录")

# 迁移项目最新更新数据
print("开始迁移项目最新更新数据...")
mysql_cursor.execute('''
SELECT id, project_id, update_content, update_date, updated_by, update_time 
FROM latest_update
''')
latest_updates = mysql_cursor.fetchall()
for update in latest_updates:
    # 转换时间类型
    update_data = list(update)
    update_data[5] = convert_time(update_data[5])  # update_time
    sqlite_cursor.execute('''
    INSERT INTO latest_update (id, project_id, update_content, update_date, updated_by, update_time) 
    VALUES (?, ?, ?, ?, ?, ?)
    ''', update_data)
sqlite_conn.commit()
print(f"迁移了 {len(latest_updates)} 条项目最新更新记录")

# 迁移待办事项数据
print("开始迁移待办事项数据...")
mysql_cursor.execute('''
SELECT id, item, create_at, is_finished, finish_at, created_by 
FROM todos
''')
todos = mysql_cursor.fetchall()
for todo in todos:
    sqlite_cursor.execute('''
    INSERT INTO todos (id, item, create_at, is_finished, finish_at, created_by) 
    VALUES (?, ?, ?, ?, ?, ?)
    ''', todo)
sqlite_conn.commit()
print(f"迁移了 {len(todos)} 条待办事项")

# 迁移工作日志数据
print("开始迁移工作日志数据...")
mysql_cursor.execute('''
SELECT id, today_activities, user, work_log_by_ai, log_date, log_time, created_by_ai 
FROM work_log
''')
work_logs = mysql_cursor.fetchall()
for log in work_logs:
    # 转换时间类型
    log_data = list(log)
    log_data[5] = convert_time(log_data[5])  # log_time
    sqlite_cursor.execute('''
    INSERT INTO work_log (id, today_activities, user, work_log_by_ai, log_date, log_time, created_by_ai) 
    VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', log_data)
sqlite_conn.commit()
print(f"迁移了 {len(work_logs)} 条工作日志")

# 关闭连接
mysql_cursor.close()
mysql_conn.close()
sqlite_cursor.close()
sqlite_conn.close()

print("数据迁移完成！")
print(f"SQLite数据库文件位置: {sqlite_db_path}")
