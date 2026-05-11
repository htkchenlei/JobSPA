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
# 优先使用环境变量 DATABASE_URL，否则使用默认路径
default_db_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'projectmanagement.db')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', f'sqlite:///{default_db_path}')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# 配置密钥
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev_secret_key_change_in_production')

# 配置文件上传大小限制（200M）
app.config['MAX_CONTENT_LENGTH'] = 200 * 1024 * 1024

# 配置上传目录
app.config['UPLOAD_FOLDER'] = os.getenv('UPLOAD_FOLDER', os.path.join(os.path.dirname(os.path.dirname(__file__)), 'uploads'))

# 初始化数据库
db = SQLAlchemy(app)

# 导入模型
from .models.models import User, Project, ProjectProgress, LatestUpdate, Todo, WorkLog

# 打印配置信息
print(f"=" * 50)
print(f"JobSPA 配置信息:")
print(f"数据库: {app.config['SQLALCHEMY_DATABASE_URI']}")
print(f"上传目录: {app.config['UPLOAD_FOLDER']}")
print(f"=" * 50)

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

# 配置前端静态文件路径
# Docker 环境: /app/frontend/dist
# 本地开发: ../frontend/dist
frontend_dist = os.path.abspath(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'frontend', 'dist'))
if not os.path.exists(frontend_dist):
    frontend_dist = os.path.abspath(os.path.join(os.path.dirname(os.path.dirname(__file__)), '..', 'frontend', 'dist'))

print(f"前端静态文件目录: {frontend_dist}")

# 为静态文件提供服务
@app.route('/static/<path:path>')
def serve_static(path):
    return send_from_directory(os.path.join(frontend_dist, 'assets'), path)

# 为前端路由提供服务（SPA 路由支持）
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve_frontend(path):
    # 如果请求的是静态文件，直接返回
    if path and os.path.exists(os.path.join(frontend_dist, path)):
        return send_from_directory(frontend_dist, path)
    # 否则返回 index.html（SPA 路由）
    return send_from_directory(frontend_dist, 'index.html')

__all__ = ['app', 'db']
