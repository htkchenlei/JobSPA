from flask import Blueprint, request, jsonify
from ..models.models import User, WorkLog, ProjectProgress
from .. import db
from datetime import datetime, date, time

# 创建蓝图
bp = Blueprint('work_log', __name__, url_prefix='/api/work-log')

# 获取工作日志列表
@bp.route('/', methods=['GET'])
def get_work_logs():
    logs = WorkLog.query.all()
    result = []
    for log in logs:
        result.append({
            'id': log.id,
            'today_activities': log.today_activities,
            'user': log.user,
            'work_log_by_ai': log.work_log_by_ai,
            'log_date': log.log_date.isoformat() if log.log_date else None,
            'log_time': log.log_time.isoformat() if log.log_time else None,
            'created_by_ai': log.created_by_ai
        })
    return jsonify(result), 200

# 获取用户的工作日志
@bp.route('/user/<int:user_id>', methods=['GET'])
def get_user_work_logs(user_id):
    logs = WorkLog.query.filter_by(user=user_id).all()
    result = []
    for log in logs:
        result.append({
            'id': log.id,
            'today_activities': log.today_activities,
            'work_log_by_ai': log.work_log_by_ai,
            'log_date': log.log_date.isoformat() if log.log_date else None,
            'log_time': log.log_time.isoformat() if log.log_time else None,
            'created_by_ai': log.created_by_ai
        })
    return jsonify(result), 200

# 获取指定日期的工作日志
@bp.route('/date/<string:log_date>', methods=['GET'])
def get_work_log_by_date(log_date):
    try:
        target_date = datetime.strptime(log_date, '%Y-%m-%d').date()
        log = WorkLog.query.filter_by(log_date=target_date).first()
        if not log:
            return jsonify({'error': '工作日志不存在'}), 404
        return jsonify({
            'id': log.id,
            'today_activities': log.today_activities,
            'user': log.user,
            'work_log_by_ai': log.work_log_by_ai,
            'log_date': log.log_date.isoformat() if log.log_date else None,
            'log_time': log.log_time.isoformat() if log.log_time else None,
            'created_by_ai': log.created_by_ai
        }), 200
    except ValueError:
        return jsonify({'error': '日期格式错误'}), 400

# 生成今日活动记录
@bp.route('/generate-activities', methods=['POST'])
def generate_today_activities():
    try:
        data = request.get_json()
        user_id = data.get('user_id')
        
        if not user_id:
            return jsonify({'error': '缺少用户ID'}), 400
        
        # 检查用户是否存在
        user = User.query.filter_by(id=user_id).first()
        if not user:
            return jsonify({'error': '用户不存在'}), 404
        
        # 获取今天的日期
        today = date.today()
        
        # 获取今天的项目更新
        today_updates = ProjectProgress.query.filter_by(update_date=today).all()
        
        # 按项目分组构建活动记录
        project_activities = {}
        for update in today_updates:
            project_name = update.project.name
            if project_name not in project_activities:
                project_activities[project_name] = []
            project_activities[project_name].append(update.update_content)
        
        # 构建最终的活动记录列表
        activities = []
        for project_name, updates in project_activities.items():
            if len(updates) == 1:
                activities.append(f"{project_name}: {updates[0]}")
            else:
                activity_str = f"{project_name}:"
                for update in updates:
                    activity_str += f"\n- {update}"
                activities.append(activity_str)
        
        # 检查是否已经存在今天的工作日志
        existing_log = WorkLog.query.filter_by(user=user_id, log_date=today).first()
        
        if existing_log:
            # 更新现有记录
            existing_log.today_activities = '\n'.join(activities)
            existing_log.log_time = datetime.now().time()
        else:
            # 创建新记录
            new_log = WorkLog(
                today_activities='\n'.join(activities),
                user=user_id,
                log_date=today,
                log_time=datetime.now().time(),
                created_by_ai='DeepSeek'
            )
            db.session.add(new_log)
        
        db.session.commit()
        
        return jsonify({
            'message': '活动记录生成成功',
            'activities': activities
        }), 200
    except Exception as e:
        print(f"生成活动记录失败: {e}")
        return jsonify({'error': '生成活动记录失败'}), 500

# 保存工作日志
@bp.route('/save', methods=['POST'])
def save_work_log():
    try:
        data = request.get_json()
        user_id = data.get('user_id')
        work_log_by_ai = data.get('work_log_by_ai')
        today_activities = data.get('today_activities', '')
        
        if not user_id or not work_log_by_ai:
            return jsonify({'error': '缺少必要参数'}), 400
        
        # 检查用户是否存在
        user = User.query.filter_by(id=user_id).first()
        if not user:
            return jsonify({'error': '用户不存在'}), 404
        
        # 获取今天的日期
        today = date.today()
        
        # 检查是否已经存在今天的工作日志
        existing_log = WorkLog.query.filter_by(user=user_id, log_date=today).first()
        
        if existing_log:
            # 更新现有记录
            existing_log.work_log_by_ai = work_log_by_ai
            existing_log.log_time = datetime.now().time()
            # 如果传递了活动记录，则更新
            if today_activities:
                existing_log.today_activities = today_activities
        else:
            # 创建新记录
            new_log = WorkLog(
                today_activities=today_activities,
                user=user_id,
                work_log_by_ai=work_log_by_ai,
                log_date=today,
                log_time=datetime.now().time(),
                created_by_ai='DeepSeek'
            )
            db.session.add(new_log)
        
        db.session.commit()
        
        return jsonify({'message': '工作日志保存成功'}), 200
    except Exception as e:
        print(f"保存工作日志失败: {e}")
        return jsonify({'error': '保存工作日志失败'}), 500

# 获取今日活动记录
@bp.route('/today-activities', methods=['GET'])
def get_today_activities():
    try:
        # 获取今天的日期
        today = date.today()
        
        # 获取今天的项目更新，按项目ID分组
        today_updates = ProjectProgress.query.filter_by(update_date=today).all()
        
        # 按项目分组构建活动记录
        project_activities = {}
        for update in today_updates:
            project_name = update.project.name
            if project_name not in project_activities:
                project_activities[project_name] = []
            project_activities[project_name].append(update.update_content)
        
        # 构建最终的活动记录列表
        activities = []
        for project_name, updates in project_activities.items():
            if len(updates) == 1:
                activities.append(f"{project_name}: {updates[0]}")
            else:
                activity_str = f"{project_name}:"
                for update in updates:
                    activity_str += f"\n- {update}"
                activities.append(activity_str)
        
        return jsonify(activities), 200
    except Exception as e:
        print(f"获取今日活动记录失败: {e}")
        return jsonify({'error': '获取今日活动记录失败'}), 500
