from flask import Flask, send_from_directory
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 创建Flask应用
app = Flask(__name__)

# 配置CORS
CORS(app, resources={r"/api/*": {"origins": "*"}})

# 配置数据库连接
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///D:\\Python\\JobSPA\\backend\\app\\jobspa.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# 配置文件上传大小限制（200M）
app.config['MAX_CONTENT_LENGTH'] = 200 * 1024 * 1024

# 初始化数据库
db = SQLAlchemy(app)

# 导入模型
from .models.models import User, Project, ProjectProgress, LatestUpdate, Todo, WorkLog

# 打印数据库文件路径
import os
from sqlalchemy import create_engine
engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
if 'sqlite' in app.config['SQLALCHEMY_DATABASE_URI']:
    # 提取SQLite数据库文件路径
    import re
    match = re.search(r'sqlite:///(.*)', app.config['SQLALCHEMY_DATABASE_URI'])
    if match:
        db_path = match.group(1)
        # 处理Windows路径
        db_path = db_path.replace('/', '\\')
        print(f"SQLite数据库文件路径: {db_path}")
        print(f"数据库文件是否存在: {os.path.exists(db_path)}")
        print(f"数据库文件大小: {os.path.getsize(db_path) if os.path.exists(db_path) else '0'} bytes")
        
        # 测试数据库连接
        from sqlalchemy import text
        try:
            with engine.connect() as conn:
                result = conn.execute(text("SELECT count(*) FROM projects"))
                print(f"\n项目表中的记录数: {result.scalar()}")
                
                result = conn.execute(text("SELECT count(*) FROM users"))
                print(f"用户表中的记录数: {result.scalar()}")
        except Exception as e:
            print(f"数据库连接失败: {str(e)}")

# 导入路由
from .routes import project_routes
from .routes import user_routes
from .routes import auth_routes
from .routes import todo_routes
from .routes import file_routes
from .routes import ai_routes
from .routes import work_log_routes
from .routes import place_routes
from .routes import file_parse_routes
from .routes import excel_process_routes

# 注册路由
app.register_blueprint(project_routes.bp)
app.register_blueprint(user_routes.bp)
app.register_blueprint(auth_routes.bp)
app.register_blueprint(todo_routes.bp)
app.register_blueprint(file_routes.bp)
app.register_blueprint(ai_routes.bp)
app.register_blueprint(work_log_routes.bp)
app.register_blueprint(place_routes.place_bp)
app.register_blueprint(file_parse_routes.file_parse_bp, url_prefix='/api')
app.register_blueprint(excel_process_routes.excel_process_bp, url_prefix='/api')

# 配置静态文件路径
frontend_dist = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'frontend', 'dist')
print(f"Frontend dist path: {frontend_dist}")

# 为静态文件提供服务
@app.route('/static/<path:path>')
def serve_static(path):
    return send_from_directory(os.path.join(frontend_dist, 'assets'), path)

# 为前端路由提供服务
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve_frontend(path):
    if path and os.path.exists(os.path.join(frontend_dist, path)):
        return send_from_directory(frontend_dist, path)
    return send_from_directory(frontend_dist, 'index.html')

__all__ = ['app', 'db']