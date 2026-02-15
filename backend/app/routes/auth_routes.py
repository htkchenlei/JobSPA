from flask import Blueprint, request, jsonify
from ..models.models import User
from .. import db
import jwt
import os
from datetime import datetime, timedelta
from dotenv import load_dotenv
from werkzeug.security import check_password_hash

# 加载环境变量
load_dotenv()

# 创建蓝图
bp = Blueprint('auth', __name__, url_prefix='/api/auth')

# 生成JWT token
def generate_token(user_id):
    # 设置token过期时间为24小时
    payload = {
        'user_id': user_id,
        'exp': datetime.utcnow() + timedelta(hours=24)
    }
    # 使用密钥生成token
    token = jwt.encode(payload, os.getenv('SECRET_KEY', 'your-secret-key'), algorithm='HS256')
    return token

# 登录接口
@bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    if not data:
        return jsonify({'error': '缺少请求数据'}), 400
    
    username = data.get('username')
    password = data.get('password')
    
    if not username or not password:
        return jsonify({'error': '用户名和密码不能为空'}), 400
    
    # 查找用户
    user = User.query.filter_by(username=username).first()
    if not user:
        return jsonify({'error': '用户名或密码错误'}), 401
    
    # 验证密码（使用哈希验证）
    if not check_password_hash(user.password, password):
        return jsonify({'error': '用户名或密码错误'}), 401
    
    # 生成token
    token = generate_token(user.id)
    
    return jsonify({
        'token': token,
        'user': {
            'id': user.id,
            'username': user.username,
            'is_admin': user.is_admin
        }
    }), 200

# 验证token接口
@bp.route('/verify', methods=['GET'])
def verify():
    token = request.headers.get('Authorization')
    if not token:
        return jsonify({'error': '缺少token'}), 401
    
    # 移除Bearer前缀
    if token.startswith('Bearer '):
        token = token.split(' ')[1]
    
    try:
        # 解码token
        payload = jwt.decode(token, os.getenv('SECRET_KEY', 'your-secret-key'), algorithms=['HS256'])
        user_id = payload.get('user_id')
        
        # 查找用户
        user = User.query.filter_by(id=user_id).first()
        if not user:
            return jsonify({'error': '用户不存在'}), 401
        
        return jsonify({
            'user': {
                'id': user.id,
                'username': user.username,
                'is_admin': user.is_admin
            }
        }), 200
    except jwt.ExpiredSignatureError:
        return jsonify({'error': 'token已过期'}), 401
    except jwt.InvalidTokenError:
        return jsonify({'error': '无效的token'}), 401

# 登出接口
@bp.route('/logout', methods=['POST'])
def logout():
  # 前端删除localStorage中的token即可，后端不需要特殊处理
  return jsonify({'message': '登出成功'}), 200

# 修改密码接口
@bp.route('/change-password', methods=['POST'])
def change_password():
  token = request.headers.get('Authorization')
  if not token:
    return jsonify({'error': '缺少token'}), 401
  
  # 移除Bearer前缀
  if token.startswith('Bearer '):
    token = token.split(' ')[1]
  
  try:
    # 解码token
    payload = jwt.decode(token, os.getenv('SECRET_KEY', 'your-secret-key'), algorithms=['HS256'])
    user_id = payload.get('user_id')
    
    # 查找用户
    user = User.query.filter_by(id=user_id).first()
    if not user:
      return jsonify({'error': '用户不存在'}), 401
    
    # 获取请求数据
    data = request.get_json()
    if not data:
      return jsonify({'error': '缺少请求数据'}), 400
    
    current_password = data.get('currentPassword')
    new_password = data.get('newPassword')
    
    if not current_password or not new_password:
      return jsonify({'error': '当前密码和新密码不能为空'}), 400
    
    # 验证当前密码
    if not check_password_hash(user.password, current_password):
      return jsonify({'error': '当前密码错误'}), 401
    
    # 更新密码
    from werkzeug.security import generate_password_hash
    user.password = generate_password_hash(new_password)
    db.session.commit()
    
    return jsonify({'message': '密码修改成功'}), 200
  except jwt.ExpiredSignatureError:
    return jsonify({'error': 'token已过期'}), 401
  except jwt.InvalidTokenError:
    return jsonify({'error': '无效的token'}), 401
  except Exception as e:
    return jsonify({'error': f'修改密码失败: {str(e)}'}), 500
