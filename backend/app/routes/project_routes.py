from flask import Blueprint, request, jsonify
from ..models.models import User, Project, ProjectProgress, LatestUpdate
from .. import db
from datetime import datetime, date, time

# 创建蓝图
bp = Blueprint('projects', __name__, url_prefix='/api/projects')

# 项目阶段映射
STAGE_MAP = {
    1: '立项中|初步沟通',
    2: '立项中|提交立项申请',
    3: '已立项|编制解决方案',
    4: '已立项|编制设计方案',
    5: '已立项|编制招投标参数',
    6: '招投标|编制参数',
    7: '招投标|已挂网',
    8: '招投标|等待结果',
    9: '已中标|已公示',
    10: '已中标|已获取中标通知书',
    11: '已中标|签署合同',
    12: '已完成|转入项目实施',
    13: '已完成|项目结束'
}

# 获取项目列表
@bp.route('/', methods=['GET'])
def get_projects():
    projects = Project.query.filter_by(is_deleted=False).all()
    result = []
    for project in projects:
        stage_int = int(project.stage)
        stage_text = STAGE_MAP.get(stage_int, '未知阶段')
        # 只显示"|"前面的内容
        if '|' in stage_text:
            stage_text = stage_text.split('|')[0]
        print(stage_text)
        
        # 获取负责人用户名
        owner_username = None
        if project.owner:
            owner_user = User.query.filter_by(id=project.owner).first()
            if owner_user:
                owner_username = owner_user.username
        
        # 获取该项目的最新更新信息
        latest_update = LatestUpdate.query.filter_by(project_id=project.id).first()
        update_content = latest_update.update_content if latest_update else '暂无更新'
        update_date = latest_update.update_date.strftime('%Y-%m-%d') if (latest_update and latest_update.update_date) else '暂无更新'
        update_time = latest_update.update_time.strftime('%H:%M:%S') if (latest_update and latest_update.update_time) else '暂无更新'
        updated_by = latest_update.updated_by if latest_update else None
        
        result.append({
            'id': project.id,
            'name': project.name,
            'client_name': project.client_name,
            'scale': project.scale,
            'start_date': project.start_date.strftime('%Y-%m-%d') if project.start_date else None,
            'location': project.location,
            'sales_person': project.sales_person,
            'stage': stage_int,
            'stage_text': stage_text,
            'owner': project.owner,
            'owner_username': owner_username,
            'province': project.province,
            'city': project.city,
            'district': project.district,
            'latest_update': {
                'content': update_content,
                'date': update_date,
                'time': update_time,
                'by': updated_by
            }
        })
    return jsonify(result), 200

# 获取单个项目
@bp.route('/<int:id>', methods=['GET'])
def get_project(id):
    project = Project.query.filter_by(id=id, is_deleted=False).first()
    if not project:
        return jsonify({'error': '项目不存在'}), 404
    
    stage_int = int(project.stage)
    stage_text = STAGE_MAP.get(stage_int, '未知阶段')
    # 只显示"|"前面的内容
    if '|' in stage_text:
        stage_text = stage_text.split('|')[0]
    
    # 获取该项目的最新更新信息
    latest_update = LatestUpdate.query.filter_by(project_id=project.id).first()
    update_content = latest_update.update_content if latest_update else '暂无更新'
    update_date = latest_update.update_date.strftime('%Y-%m-%d') if (latest_update and latest_update.update_date) else '暂无更新'
    update_time = latest_update.update_time.strftime('%H:%M:%S') if (latest_update and latest_update.update_time) else '暂无更新'
    updated_by = latest_update.updated_by if latest_update else None
    
    return jsonify({
        'id': project.id,
        'name': project.name,
        'client_name': project.client_name,
        'scale': project.scale,
        'start_date': project.start_date.strftime('%Y-%m-%d') if project.start_date else None,
        'location': project.location,
        'sales_person': project.sales_person,
        'stage': stage_int,
        'stage_text': stage_text,
        'owner': project.owner,
        'province': project.province,
        'city': project.city,
        'district': project.district,
        'latest_update': {
            'content': update_content,
            'date': update_date,
            'time': update_time,
            'by': updated_by
        }
    }), 200

# 创建项目
@bp.route('/', methods=['POST'])
def create_project():
    data = request.get_json()
    if not data:
        return jsonify({'error': '缺少请求数据'}), 400
    
    # 处理日期字段
    start_date_str = data.get('start_date')
    start_date = None
    if start_date_str:
        start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
    
    # 根据owner字段（用户名）查询user表，获取用户ID
    owner_name = data.get('owner')
    owner_id = 1  # 默认用户ID
    if owner_name:
        # 尝试根据用户名查询用户
        user = User.query.filter_by(username=owner_name).first()
        if user:
            owner_id = user.id
    
    new_project = Project(
        name=data.get('name'),
        client_name=data.get('client_name'),
        scale=data.get('scale'),
        start_date=start_date,
        location=data.get('location'),
        sales_person=data.get('sales_person'),
        stage=data.get('stage', 1),
        owner=owner_id,
        province=data.get('province'),
        city=data.get('city'),
        district=data.get('district')
    )
    
    db.session.add(new_project)
    db.session.commit()
    
    stage_int = int(new_project.stage)
    stage_text = STAGE_MAP.get(stage_int, '未知阶段')
    # 只显示"|"前面的内容
    if '|' in stage_text:
        stage_text = stage_text.split('|')[0]
    return jsonify({
        'id': new_project.id,
        'name': new_project.name,
        'client_name': new_project.client_name,
        'scale': new_project.scale,
        'start_date': new_project.start_date.strftime('%Y-%m-%d') if new_project.start_date else None,
        'location': new_project.location,
        'sales_person': new_project.sales_person,
        'stage': stage_int,
        'stage_text': stage_text,
        'owner': new_project.owner,
        'province': new_project.province,
        'city': new_project.city,
        'district': new_project.district
    }), 201

# 更新项目
@bp.route('/<int:id>', methods=['PUT'])
def update_project(id):
    project = Project.query.filter_by(id=id, is_deleted=False).first()
    if not project:
        return jsonify({'error': '项目不存在'}), 404
    
    data = request.get_json()
    if not data:
        return jsonify({'error': '缺少请求数据'}), 400
    
    # 处理日期字段
    start_date_str = data.get('start_date')
    if start_date_str:
        project.start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
    
    # 更新其他字段
    project.name = data.get('name', project.name)
    project.client_name = data.get('client_name', project.client_name)
    project.scale = data.get('scale', project.scale)
    project.location = data.get('location', project.location)
    project.sales_person = data.get('sales_person', project.sales_person)
    project.stage = data.get('stage', project.stage)
    
    # 根据owner字段（用户名）查询user表，获取用户ID
    owner_name = data.get('owner')
    if owner_name:
        # 尝试根据用户名查询用户
        user = User.query.filter_by(username=owner_name).first()
        if user:
            project.owner = user.id
    
    project.province = data.get('province', project.province)
    project.city = data.get('city', project.city)
    project.district = data.get('district', project.district)
    
    db.session.commit()
    
    stage_int = int(project.stage)
    stage_text = STAGE_MAP.get(stage_int, '未知阶段')
    # 只显示"|"前面的内容
    if '|' in stage_text:
        stage_text = stage_text.split('|')[0]
    return jsonify({
        'id': project.id,
        'name': project.name,
        'client_name': project.client_name,
        'scale': project.scale,
        'start_date': project.start_date.strftime('%Y-%m-%d') if project.start_date else None,
        'location': project.location,
        'sales_person': project.sales_person,
        'stage': stage_int,
        'stage_text': stage_text,
        'owner': project.owner,
        'province': project.province,
        'city': project.city,
        'district': project.district
    }), 200

# 更新项目进度
@bp.route('/<int:id>/progress', methods=['POST'])
def update_project_progress(id):
    project = Project.query.filter_by(id=id, is_deleted=False).first()
    if not project:
        return jsonify({'error': '项目不存在'}), 404
    
    data = request.get_json()
    if not data:
        return jsonify({'error': '缺少请求数据'}), 400
    
    # 获取当前日期和时间
    today = date.today()
    now = datetime.now().time()
    
    # 创建进度记录
    new_progress = ProjectProgress(
        project_id=project.id,
        update_content=data.get('update_content', ''),
        update_date=today,
        updated_by=data.get('updated_by', 1),  # 默认用户ID为1
        update_time=now,
        is_important=data.get('is_important', 0)
    )
    
    # 如果提供了新的阶段，更新项目阶段
    if 'stage' in data:
        project.stage = data['stage']
    
    # 检查latest_update表中是否已存在该项目的记录
    latest_update = LatestUpdate.query.filter_by(project_id=project.id).first()
    
    if latest_update:
        # 如果存在，更新记录
        latest_update.update_content = data.get('update_content', '')
        latest_update.update_date = today
        latest_update.updated_by = data.get('updated_by', 1)
        latest_update.update_time = now
    else:
        # 如果不存在，创建新记录
        latest_update = LatestUpdate(
            project_id=project.id,
            update_content=data.get('update_content', ''),
            update_date=today,
            updated_by=data.get('updated_by', 1),
            update_time=now
        )
        db.session.add(latest_update)
    
    db.session.add(new_progress)
    db.session.commit()
    
    stage_int = int(project.stage)
    stage_text = STAGE_MAP.get(stage_int, '未知阶段')
    # 只显示"|"前面的内容
    if '|' in stage_text:
        stage_text = stage_text.split('|')[0]
    return jsonify({
        'id': project.id,
        'stage': stage_int,
        'stage_text': stage_text,
        'progressId': new_progress.id,
        'message': '项目进度更新成功'
    }), 200

# 获取项目进度历史
@bp.route('/<int:id>/progress', methods=['GET'])
def get_project_progress(id):
    project = Project.query.filter_by(id=id, is_deleted=False).first()
    if not project:
        return jsonify({'error': '项目不存在'}), 404
    
    progresses = ProjectProgress.query.filter_by(project_id=id).order_by(ProjectProgress.update_date.desc()).all()
    result = []
    for progress in progresses:
        result.append({
            'id': progress.id,
            'update_content': progress.update_content,
            'update_date': progress.update_date.strftime('%Y-%m-%d'),
            'update_time': progress.update_time.strftime('%H:%M:%S'),
            'updated_by': progress.updated_by,
            'is_important': progress.is_important
        })
    
    return jsonify(result), 200

# 删除项目（软删除）
@bp.route('/<int:id>', methods=['DELETE'])
def delete_project(id):
    project = Project.query.filter_by(id=id, is_deleted=False).first()
    if not project:
        return jsonify({'error': '项目不存在'}), 404
    
    project.is_deleted = True
    db.session.commit()
    
    return jsonify({'message': '项目删除成功'}), 200

# 恢复项目（仅admin）
@bp.route('/<int:id>/restore', methods=['POST'])
def restore_project(id):
    project = Project.query.filter_by(id=id, is_deleted=True).first()
    if not project:
        return jsonify({'error': '项目不存在或未被删除'}), 404
    
    # 这里可以添加admin权限验证
    
    project.is_deleted = False
    db.session.commit()
    
    return jsonify({'message': '项目恢复成功'}), 200

# 获取项目阶段列表
@bp.route('/stages', methods=['GET'])
def get_project_stages():
    result = []
    for stage, text in STAGE_MAP.items():
        # 只显示"|"前面的内容
        display_text = text
        if '|' in display_text:
            display_text = display_text.split('|')[0]
        result.append({
            'value': stage,
            'label': display_text
        })
    return jsonify(result), 200

# 关键词搜索
@bp.route('/search', methods=['POST'])
def search_projects():
    data = request.get_json()
    if not data:
        return jsonify({'error': '缺少请求数据'}), 400
    
    keywords = data.get('keywords', '')
    start_date = data.get('start_date')
    end_date = data.get('end_date')
    
    # 处理关键词
    keyword_list = [k.strip() for k in keywords.split() if k.strip()]
    
    # 构建查询
    from sqlalchemy import or_
    
    # 从projects表中搜索name字段
    project_query = Project.query.filter_by(is_deleted=False)
    if keyword_list:
        project_filters = []
        for keyword in keyword_list:
            project_filters.append(Project.name.ilike(f'%{keyword}%'))
        project_query = project_query.filter(or_(*project_filters))
    
    # 从project_progress表中搜索update_content字段，然后关联到projects表
    from sqlalchemy.orm import joinedload
    progress_query = ProjectProgress.query
    if keyword_list:
        progress_filters = []
        for keyword in keyword_list:
            progress_filters.append(ProjectProgress.update_content.ilike(f'%{keyword}%'))
        progress_query = progress_query.filter(or_(*progress_filters))
    
    # 获取所有匹配的项目ID
    project_ids = set()
    
    # 从projects表中获取匹配的项目ID
    for project in project_query.all():
        project_ids.add(project.id)
    
    # 从project_progress表中获取匹配的项目ID
    for progress in progress_query.all():
        project_ids.add(progress.project_id)
    
    # 查询所有匹配的项目
    if project_ids:
        projects = Project.query.filter(Project.id.in_(project_ids), Project.is_deleted == False).all()
    else:
        projects = []
    
    # 构建返回结果
    result = []
    for project in projects:
        stage_int = int(project.stage)
        stage_text = STAGE_MAP.get(stage_int, '未知阶段')
        # 只显示"|"前面的内容
        if '|' in stage_text:
            stage_text = stage_text.split('|')[0]
        
        result.append({
            'id': project.id,
            'name': project.name,
            'client_name': project.client_name,
            'scale': project.scale,
            'start_date': project.start_date.strftime('%Y-%m-%d') if project.start_date else None,
            'location': project.location,
            'sales_person': project.sales_person,
            'stage': stage_int,
            'stage_text': stage_text,
            'owner': project.owner,
            'province': project.province,
            'city': project.city,
            'district': project.district
        })
    
    return jsonify(result), 200

# 获取今天的项目更新
@bp.route('/today-updates', methods=['GET'])
def get_today_updates():
    from datetime import date
    today = date.today()
    
    # 从project_progress表中查询今天的更新，关联projects表获取项目名称
    from sqlalchemy.orm import joinedload
    
    # 构建查询
    updates = ProjectProgress.query\
        .filter_by(update_date=today)\
        .options(joinedload(ProjectProgress.project))\
        .all()
    
    # 构建返回结果
    result = []
    for update in updates:
        if update.project and not update.project.is_deleted:
            result.append({
                'id': update.id,
                'project_id': update.project_id,
                'project_name': update.project.name,
                'update_content': update.update_content,
                'update_date': update.update_date.strftime('%Y-%m-%d'),
                'update_time': update.update_time.strftime('%H:%M:%S'),
                'updated_by': update.updated_by
            })
    
    return jsonify(result), 200