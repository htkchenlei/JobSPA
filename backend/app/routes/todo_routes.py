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
    
    # 使用SQLAlchemy引擎直接执行SQL语句
    from sqlalchemy import create_engine, text
    from app import app
    engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
    
    with engine.connect() as conn:
        # 构建查询语句
        if is_finished is not None:
            query = text(f"SELECT id, item, is_finished, create_at, finish_at FROM todos WHERE created_by = {user_id} AND is_finished = {1 if is_finished else 0}")
        else:
            query = text(f"SELECT id, item, is_finished, create_at, finish_at FROM todos WHERE created_by = {user_id}")
        
        result = conn.execute(query)
        todos = result.fetchall()
        
        response = []
        for todo in todos:
            # 检查日期类型
            if isinstance(todo[3], str):
                create_at = todo[3]
            else:
                create_at = todo[3].strftime('%Y-%m-%d %H:%M:%S')
            
            if todo[4]:
                if isinstance(todo[4], str):
                    finish_at = todo[4]
                else:
                    finish_at = todo[4].strftime('%Y-%m-%d %H:%M:%S')
            else:
                finish_at = None
            
            response.append({
                'id': todo[0],
                'item': todo[1],
                'is_finished': bool(todo[2]),
                'create_at': create_at,
                'finish_at': finish_at
            })
    
    return jsonify(response), 200

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