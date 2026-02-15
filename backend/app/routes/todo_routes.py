from flask import Blueprint, request, jsonify
from ..models.models import Todo
from .. import db
from datetime import datetime, timedelta
import jwt
import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 东八区时间偏移量
EAST_8_OFFSET = timedelta(hours=8)

# 获取当前东八区时间
def get_east_8_time():
    return datetime.utcnow() + EAST_8_OFFSET

# 从请求中获取当前用户ID
def get_current_user_id():
    token = request.headers.get('Authorization')
    if not token:
        return None
    
    # 移除Bearer前缀
    if token.startswith('Bearer '):
        token = token.split(' ')[1]
    
    try:
        # 解码token
        payload = jwt.decode(token, os.getenv('SECRET_KEY', 'your-secret-key'), algorithms=['HS256'])
        user_id = payload.get('user_id')
        return user_id
    except Exception as e:
        return None

# 创建蓝图
bp = Blueprint('todos', __name__, url_prefix='/api/todos')

# 获取待办事项列表
@bp.route('/', methods=['GET'])
def get_todos():
    # 获取查询参数
    is_finished = request.args.get('is_finished', type=lambda x: x.lower() == 'true')
    
    # 从请求中获取用户ID
    user_id = get_current_user_id()
    if not user_id:
        return jsonify({'error': '未授权访问'}), 401
    
    query = Todo.query.filter_by(created_by=user_id)
    
    if is_finished is not None:
        query = query.filter_by(is_finished=is_finished)
    
    todos = query.all()
    
    result = []
    for todo in todos:
        result.append({
            'id': todo.id,
            'item': todo.item,
            'is_finished': todo.is_finished,
            'create_at': todo.create_at.strftime('%Y-%m-%d %H:%M:%S'),
            'finish_at': todo.finish_at.strftime('%Y-%m-%d %H:%M:%S') if todo.finish_at else None
        })
    
    return jsonify(result), 200

# 获取单个待办事项
@bp.route('/<int:id>', methods=['GET'])
def get_todo(id):
    # 从请求中获取用户ID
    user_id = get_current_user_id()
    if not user_id:
        return jsonify({'error': '未授权访问'}), 401
    
    todo = Todo.query.filter_by(id=id, created_by=user_id).first()
    if not todo:
        return jsonify({'error': '待办事项不存在'}), 404
    
    return jsonify({
        'id': todo.id,
        'item': todo.item,
        'is_finished': todo.is_finished,
        'create_at': todo.create_at.strftime('%Y-%m-%d %H:%M:%S'),
        'finish_at': todo.finish_at.strftime('%Y-%m-%d %H:%M:%S') if todo.finish_at else None
    }), 200

# 创建待办事项
@bp.route('/', methods=['POST'])
def create_todo():
    data = request.get_json()
    if not data:
        return jsonify({'error': '缺少请求数据'}), 400
    
    # 从请求中获取用户ID
    user_id = get_current_user_id()
    if not user_id:
        return jsonify({'error': '未授权访问'}), 401
    
    new_todo = Todo(
        item=data.get('item'),
        created_by=user_id
    )
    
    db.session.add(new_todo)
    db.session.commit()
    
    return jsonify({
        'id': new_todo.id,
        'item': new_todo.item,
        'is_finished': new_todo.is_finished,
        'create_at': new_todo.create_at.strftime('%Y-%m-%d %H:%M:%S')
    }), 201

# 更新待办事项
@bp.route('/<int:id>', methods=['PUT'])
def update_todo(id):
    # 从请求中获取用户ID
    user_id = get_current_user_id()
    if not user_id:
        return jsonify({'error': '未授权访问'}), 401
    
    todo = Todo.query.filter_by(id=id, created_by=user_id).first()
    if not todo:
        return jsonify({'error': '待办事项不存在'}), 404
    
    data = request.get_json()
    if not data:
        return jsonify({'error': '缺少请求数据'}), 400
    
    # 更新待办事项内容
    if 'item' in data:
        todo.item = data['item']
    
    # 如果is_finished状态改变
    if 'is_finished' in data and data['is_finished'] != todo.is_finished:
        todo.is_finished = data['is_finished']
        if todo.is_finished:
            todo.finish_at = datetime.utcnow()
        else:
            todo.finish_at = None
    
    db.session.commit()
    
    return jsonify({
        'id': todo.id,
        'item': todo.item,
        'is_finished': todo.is_finished,
        'create_at': todo.create_at.strftime('%Y-%m-%d %H:%M:%S'),
        'finish_at': todo.finish_at.strftime('%Y-%m-%d %H:%M:%S') if todo.finish_at else None
    }), 200

# 标记待办事项为完成
@bp.route('/<int:id>/complete', methods=['POST'])
def complete_todo(id):
    # 从请求中获取用户ID
    user_id = get_current_user_id()
    if not user_id:
        return jsonify({'error': '未授权访问'}), 401
    
    todo = Todo.query.filter_by(id=id, created_by=user_id).first()
    if not todo:
        return jsonify({'error': '待办事项不存在'}), 404
    
    if todo.is_finished:
        return jsonify({'error': '待办事项已经完成'}), 400
    
    todo.is_finished = True
    todo.finish_at = get_east_8_time()
    db.session.commit()
    
    return jsonify({
        'id': todo.id,
        'is_finished': todo.is_finished,
        'finish_at': todo.finish_at.strftime('%Y-%m-%d %H:%M:%S'),
        'message': '待办事项标记为完成'
    }), 200

# 标记待办事项为未完成
@bp.route('/<int:id>/uncomplete', methods=['POST'])
def uncomplete_todo(id):
    # 从请求中获取用户ID
    user_id = get_current_user_id()
    if not user_id:
        return jsonify({'error': '未授权访问'}), 401
    
    todo = Todo.query.filter_by(id=id, created_by=user_id).first()
    if not todo:
        return jsonify({'error': '待办事项不存在'}), 404
    
    if not todo.is_finished:
        return jsonify({'error': '待办事项尚未完成'}), 400
    
    todo.is_finished = False
    todo.finish_at = None
    db.session.commit()
    
    return jsonify({
        'id': todo.id,
        'is_finished': todo.is_finished,
        'finish_at': None,
        'message': '待办事项标记为未完成'
    }), 200

# 删除待办事项
@bp.route('/<int:id>', methods=['DELETE'])
def delete_todo(id):
    # 从请求中获取用户ID
    user_id = get_current_user_id()
    if not user_id:
        return jsonify({'error': '未授权访问'}), 401
    
    todo = Todo.query.filter_by(id=id, created_by=user_id).first()
    if not todo:
        return jsonify({'error': '待办事项不存在'}), 404
    
    db.session.delete(todo)
    db.session.commit()
    
    return jsonify({'message': '待办事项删除成功'}), 200