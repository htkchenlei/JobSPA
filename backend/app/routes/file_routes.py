from flask import Blueprint, request, jsonify, send_file
from .. import db
import os
import jwt
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 创建蓝图
bp = Blueprint('files', __name__, url_prefix='/api/files')

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

# 获取文件根目录
def get_root_directory():
    # 从环境变量获取根目录，或者使用默认值
    root_dir = os.getenv('FILE_ROOT_DIRECTORY', os.path.join(os.path.dirname(__file__), '..', '..', 'uploads'))
    print(f"File root directory: {root_dir}")
    return root_dir

# 确保目录存在
def ensure_directory_exists(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

# 获取文件系统数据
@bp.route('/', methods=['GET'])
def get_file_system():
    user_id = get_current_user_id()
    if not user_id:
        return jsonify({'error': '未授权访问'}), 401
    root_dir = get_root_directory()
    
    # 为每个用户创建独立的文件目录
    user_dir = os.path.join(root_dir, f'user_{user_id}')
    ensure_directory_exists(user_dir)
    
    # 构建文件系统树
    def build_tree(directory, base_path=''):
        tree = {
            'id': base_path or 'root',
            'name': os.path.basename(directory) or '根目录',
            'type': 'folder',
            'expanded': True,
            'children': []
        }
        
        try:
            for item in os.listdir(directory):
                item_path = os.path.join(directory, item)
                relative_path = os.path.join(base_path, item) if base_path else item
                
                if os.path.isdir(item_path):
                    tree['children'].append(build_tree(item_path, relative_path))
                else:
                    # 获取文件信息
                    file_stats = os.stat(item_path)
                    file_size = file_stats.st_size
                    
                    # 格式化文件大小
                    def format_size(size):
                        if size < 1024:
                            return f'{size}B'
                        elif size < 1024 * 1024:
                            return f'{(size / 1024):.1f}KB'
                        else:
                            return f'{(size / (1024 * 1024)):.1f}MB'
                    
                    tree['children'].append({
                        'id': relative_path,
                        'name': item,
                        'type': 'file',
                        'size': format_size(file_size),
                        'path': relative_path
                    })
        except PermissionError:
            pass
        
        return tree
    
    file_system = build_tree(user_dir)
    return jsonify(file_system), 200

# 创建文件夹
@bp.route('/folders', methods=['POST'])
def create_folder():
    user_id = get_current_user_id()
    if not user_id:
        return jsonify({'error': '未授权访问'}), 401
    root_dir = get_root_directory()
    user_dir = os.path.join(root_dir, f'user_{user_id}')
    
    # 确保用户目录存在
    ensure_directory_exists(user_dir)
    
    data = request.get_json()
    if not data or 'name' not in data:
        return jsonify({'error': '缺少文件夹名称'}), 400
    
    folder_name = data['name']
    parent_id = data.get('parentId', 'root')
    
    # 构建文件夹路径
    if parent_id == 'root':
        folder_path = os.path.join(user_dir, folder_name)
    else:
        # 对于非根目录，需要确保parent_id是有效的路径
        # 移除可能的路径分隔符，确保只创建文件夹
        safe_parent_id = parent_id.replace('/', os.sep).replace('\\', os.sep)
        folder_path = os.path.join(user_dir, safe_parent_id, folder_name)
    
    try:
        os.makedirs(folder_path, exist_ok=True)
        return jsonify({'message': '文件夹创建成功', 'path': folder_path}), 201
    except Exception as e:
        return jsonify({'error': f'创建文件夹失败: {str(e)}'}), 500

# 上传文件
@bp.route('/upload', methods=['POST'])
def upload_file():
    user_id = get_current_user_id()
    if not user_id:
        return jsonify({'error': '未授权访问'}), 401
    root_dir = get_root_directory()
    user_dir = os.path.join(root_dir, f'user_{user_id}')
    
    if 'files' not in request.files:
        return jsonify({'error': '缺少文件'}), 400
    
    folder_id = request.form.get('folderId', 'root')
    
    # 构建上传目录路径
    if folder_id == 'root':
        upload_dir = user_dir
    else:
        upload_dir = os.path.join(user_dir, folder_id)
    
    ensure_directory_exists(upload_dir)
    
    uploaded_files = []
    
    for file in request.files.getlist('files'):
        if file.filename:
            file_path = os.path.join(upload_dir, file.filename)
            try:
                file.save(file_path)
                uploaded_files.append({
                    'name': file.filename,
                    'path': os.path.join(folder_id, file.filename) if folder_id != 'root' else file.filename
                })
            except Exception as e:
                return jsonify({'error': f'上传文件失败: {str(e)}'}), 500
    
    return jsonify({'message': '文件上传成功', 'files': uploaded_files}), 201

# 删除文件或文件夹
@bp.route('/<path:path>', methods=['DELETE'])
def delete_file(path):
    user_id = get_current_user_id()
    if not user_id:
        return jsonify({'error': '未授权访问'}), 401
    root_dir = get_root_directory()
    user_dir = os.path.join(root_dir, f'user_{user_id}')
    
    # 构建完整路径
    target_path = os.path.join(user_dir, path)
    
    try:
        if os.path.isfile(target_path):
            os.remove(target_path)
            return jsonify({'message': '文件删除成功'}), 200
        elif os.path.isdir(target_path):
            import shutil
            shutil.rmtree(target_path)
            return jsonify({'message': '文件夹删除成功'}), 200
        else:
            return jsonify({'error': '文件或文件夹不存在'}), 404
    except Exception as e:
        return jsonify({'error': f'删除失败: {str(e)}'}), 500

# 下载文件
@bp.route('/download/<path:path>', methods=['GET'])
def download_file(path):
    user_id = get_current_user_id()
    if not user_id:
        return jsonify({'error': '未授权访问'}), 401
    root_dir = get_root_directory()
    user_dir = os.path.join(root_dir, f'user_{user_id}')
    
    # 构建完整路径
    file_path = os.path.join(user_dir, path)
    
    if os.path.isfile(file_path):
        return send_file(file_path, as_attachment=True)
    else:
        return jsonify({'error': '文件不存在'}), 404
