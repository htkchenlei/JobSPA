from flask import Blueprint, jsonify
from ..models.models import User

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
