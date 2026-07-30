from flask import Blueprint, jsonify
from ..models.models import User, Project, LatestUpdate
from .. import db

# 创建蓝图
bp = Blueprint('users', __name__, url_prefix='/api/users')

# 获取用户列表
@bp.route('/', methods=['GET'])
def get_users():
    users = User.query.all()
    result = []
    for user in users:
        result.append({
            'id': user.id,
            'username': user.username
        })
    return jsonify(result), 200

# 获取最近的更新记录
@bp.route('/latest-updates', methods=['GET'])
def get_latest_updates():
    try:
        # 获取最近10条更新记录，按时间倒序排列
        updates = LatestUpdate.query.order_by(
            LatestUpdate.update_date.desc(),
            LatestUpdate.update_time.desc()
        ).limit(10).all()
        
        result = []
        for update in updates:
            # 获取关联的项目名称
            project = Project.query.filter_by(id=update.project_id).first()
            project_name = project.name if project else '未知项目'
            
            # 获取更新者名称
            user = User.query.filter_by(id=update.updated_by).first()
            updated_by_name = user.username if user else '未知用户'
            
            # 格式化日期和时间
            update_date = update.update_date.strftime('%Y-%m-%d') if update.update_date else None
            update_time = update.update_time.strftime('%H:%M:%S') if update.update_time else None
            
            result.append({
                'id': update.id,
                'project_id': update.project_id,
                'project_name': project_name,
                'update_content': update.update_content,
                'update_date': update_date,
                'update_time': update_time,
                'updated_by': update.updated_by,
                'updated_by_name': updated_by_name
            })
        
        return jsonify(result), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
