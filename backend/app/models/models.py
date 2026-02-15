from .. import db
from datetime import datetime, timedelta

# 东八区时间偏移量
EAST_8_OFFSET = timedelta(hours=8)

# 获取当前东八区时间
def get_east_8_time():
    return datetime.utcnow() + EAST_8_OFFSET

# 用户模型
class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)  # hash加密存储
    is_admin = db.Column(db.Boolean, nullable=False, default=False)
    is_enable = db.Column(db.Boolean, nullable=False, default=True)
    
    # 关联的项目进度更新
    progresses = db.relationship('ProjectProgress', backref='user', lazy=True)

# 项目模型
class Project(db.Model):
    __tablename__ = 'projects'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
    client_name = db.Column(db.String(255), nullable=False)
    scale = db.Column(db.String(100), nullable=True)
    start_date = db.Column(db.Date, nullable=True)  # 仅记录日期，无时间
    location = db.Column(db.String(255), nullable=True)
    sales_person = db.Column(db.String(100), nullable=True)
    stage = db.Column(db.Integer, nullable=False, default=1)  # 项目阶段，具体含义见下方注释
    is_deleted = db.Column(db.Boolean, nullable=False, default=False)
    owner = db.Column(db.Integer, nullable=True)  # 项目负责人
    province = db.Column(db.String(100), nullable=True)
    city = db.Column(db.String(100), nullable=True)
    district = db.Column(db.String(100), nullable=True)
    
    # 项目阶段含义：
    # 1: '立项中|初步沟通'
    # 2: '立项中|提交立项申请'
    # 3: '已立项|编制解决方案'
    # 4: '已立项|编制设计方案'
    # 5: '已立项|编制招投标参数'
    # 6: '招投标|编制参数'
    # 7: '招投标|已挂网'
    # 8: '招投标|等待结果'
    # 9: '已中标|已公示'
    # 10: '已中标|已获取中标通知书'
    # 11: '已中标|签署合同'
    # 12: '已完成|转入项目实施'
    # 13: '已完成|项目结束'
    
    # 项目进展记录
    progresses = db.relationship('ProjectProgress', backref='project', lazy=True)

# 项目进展模型
class ProjectProgress(db.Model):
    __tablename__ = 'project_progress'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'), nullable=False)
    update_content = db.Column(db.Text, nullable=False)
    update_date = db.Column(db.Date, nullable=False)  # 仅记录日期，无时间
    updated_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    update_time = db.Column(db.Time, nullable=False)  # 仅记录时间，无日期
    is_important = db.Column(db.Integer, nullable=False, default=0)  # 0为不重要，1为重要

# 项目最新更新模型
class LatestUpdate(db.Model):
    __tablename__ = 'latest_update'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'), nullable=False, unique=True)
    update_content = db.Column(db.Text, nullable=False)
    update_date = db.Column(db.Date, nullable=False)  # 仅记录日期，无时间
    updated_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    update_time = db.Column(db.Time, nullable=False)  # 仅记录时间，无日期
    
    # 关联到项目
    project = db.relationship('Project', backref=db.backref('latest_update', uselist=False))
    # 关联到用户
    user = db.relationship('User', backref='latest_updates')

# 待办事项模型
class Todo(db.Model):
    __tablename__ = 'todos'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    item = db.Column(db.String(255), nullable=False)
    create_at = db.Column(db.TIMESTAMP, default=get_east_8_time)
    is_finished = db.Column(db.Boolean, default=False)
    finish_at = db.Column(db.TIMESTAMP, nullable=True)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

# 工作日志模型
class WorkLog(db.Model):
    __tablename__ = 'work_log'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    today_activities = db.Column(db.String(2000), nullable=True)
    user = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    work_log_by_ai = db.Column(db.String(2000), nullable=True)
    log_date = db.Column(db.Date, nullable=True)
    log_time = db.Column(db.Time, nullable=True)
    created_by_ai = db.Column(db.String(100), nullable=True, default='DeepSeek')
    
    # 关联到用户
    user_obj = db.relationship('User', backref='work_logs')