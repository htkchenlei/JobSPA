import sys
import os

# 添加当前目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# 从app包中导入应用实例和数据库对象
from app import app, db

# 导入模型
from app.models.models import User, Project, ProjectProgress, LatestUpdate, Todo, WorkLog

# 导入密码哈希工具
from werkzeug.security import generate_password_hash

# 创建应用上下文
with app.app_context():
    try:
        # 尝试执行一个简单的查询来验证连接
        db.session.execute('SELECT 1')
        print('数据库连接成功！')
        
        # 检查是否存在users表
        result = db.session.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='users'")
        if not result.fetchone():
            # 创建所有表
            print('数据库表结构不存在，开始创建...')
            db.create_all()
            print('数据库表结构创建成功！')
            
            # 创建默认用户
            hashed_password = generate_password_hash('123456')
            default_user = User(username='admin', password=hashed_password, is_admin=True, is_enable=True)
            db.session.add(default_user)
            db.session.commit()
            print('默认用户创建成功：用户名=admin，密码=123456')
        else:
            print('数据库表结构已存在，无需创建。')
            
        print('数据库模型已更新为用户提供的结构：')
        print('- users: 用户信息表')
        print('- projects: 项目基础信息表')
        print('- project_progress: 项目进度更新表')
        print('- latest_update: 项目最新更新表')
        print('- todos: 待办事项表')
        print('- work_log: 工作日志表')
        print('\n项目阶段含义（统一 5 档）：')
        print('1: 立项中')
        print('2: 已立项')
        print('3: 招投标')
        print('4: 已中标')
        print('5: 已完成')
    except Exception as e:
        print(f'数据库连接失败：{e}')
        print('请检查数据库连接配置和SQLite文件权限。')