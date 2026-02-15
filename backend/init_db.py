import sys
import os

# 添加当前目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# 从app包中导入应用实例和数据库对象
from app import app, db

# 导入模型
from app.models.models import User, Project, ProjectProgress

# 创建应用上下文
with app.app_context():
    # 由于数据库表结构已经存在，这里不执行create_all()
    # 只检查数据库连接
    try:
        # 尝试执行一个简单的查询来验证连接
        db.session.execute('SELECT 1')
        print('数据库连接成功！')
        print('数据库表结构已存在，无需创建。')
        print('数据库模型已更新为用户提供的结构：')
        print('- users: 用户信息表')
        print('- projects: 项目基础信息表')
        print('- project_progress: 项目进度更新表')
        print('\n项目阶段含义：')
        print('1: 立项中|初步沟通')
        print('2: 立项中|提交立项申请')
        print('3: 已立项|编制解决方案')
        print('4: 已立项|编制设计方案')
        print('5: 已立项|编制招投标参数')
        print('6: 招投标|编制参数')
        print('7: 招投标|已挂网')
        print('8: 招投标|等待结果')
        print('9: 已中标|已公示')
        print('10: 已中标|已获取中标通知书')
        print('11: 已中标|签署合同')
        print('12: 已完成|转入项目实施')
        print('13: 已完成|项目结束')
    except Exception as e:
        print(f'数据库连接失败：{e}')
        print('请检查数据库连接配置和MySQL服务状态。')