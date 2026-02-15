import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 打印当前工作目录
print(f"当前工作目录: {os.getcwd()}")

# 打印环境变量中的数据库连接字符串
print(f"环境变量中的DATABASE_URL: {os.getenv('DATABASE_URL')}")

# 计算SQLite数据库文件的绝对路径
db_url = os.getenv('DATABASE_URL', 'sqlite:///./projectmanagement.db')
if db_url.startswith('sqlite:///'):
    db_path = db_url.replace('sqlite:///', '')
    if db_path.startswith('./'):
        db_path = os.path.join(os.getcwd(), db_path[2:])
    print(f"SQLite数据库文件的绝对路径: {db_path}")
    print(f"数据库文件是否存在: {os.path.exists(db_path)}")
