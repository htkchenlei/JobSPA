from flask import Blueprint, jsonify
from ..models.models import ProjectProgress, Project, User
from .. import db
from datetime import datetime, timedelta

bp = Blueprint('public', __name__, url_prefix='/api/public')

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


@bp.route('/weekly-updates', methods=['GET'])
def get_weekly_updates():
    today = datetime.now().date()
    days_since_saturday = (today.weekday() - 5) % 7
    if days_since_saturday == 0:
        days_since_saturday = 7
    last_saturday = today - timedelta(days=days_since_saturday)

    updates = ProjectProgress.query.filter(
        ProjectProgress.update_date >= last_saturday,
        ProjectProgress.update_date <= today
    ).order_by(ProjectProgress.update_date.desc(), ProjectProgress.update_time.desc()).all()

    result = []
    for update in updates:
        project = Project.query.get(update.project_id)
        user = User.query.get(update.updated_by)
        if project and not project.is_deleted:
            result.append({
                'id': update.id,
                'project_id': update.project_id,
                'project_name': project.name,
                'client_name': project.client_name,
                'project_stage': project.stage,
                'project_stage_text': STAGE_MAP.get(project.stage, str(project.stage)),
                'update_content': update.update_content,
                'update_date': str(update.update_date),
                'update_time': str(update.update_time),
                'updated_by': user.username if user else '未知用户',
                'is_important': update.is_important
            })

    return jsonify({
        'success': True,
        'message': '获取成功',
        'data': result,
        'count': len(result),
        'time_range': {
            'start_date': str(last_saturday),
            'end_date': str(today)
        }
    })


@bp.route('/weekly-updates/count', methods=['GET'])
def get_weekly_updates_count():
    today = datetime.now().date()
    days_since_saturday = (today.weekday() - 5) % 7
    if days_since_saturday == 0:
        days_since_saturday = 7
    last_saturday = today - timedelta(days=days_since_saturday)

    count = ProjectProgress.query.filter(
        ProjectProgress.update_date >= last_saturday,
        ProjectProgress.update_date <= today
    ).count()

    return jsonify({
        'success': True,
        'count': count,
        'time_range': {
            'start_date': str(last_saturday),
            'end_date': str(today)
        }
    })


@bp.route('/monthly-updates', methods=['GET'])
def get_monthly_updates():
    """获取当月全部项目更新记录（公开接口）"""
    today = datetime.now().date()
    first_day_of_month = today.replace(day=1)

    updates = ProjectProgress.query.filter(
        ProjectProgress.update_date >= first_day_of_month,
        ProjectProgress.update_date <= today
    ).order_by(ProjectProgress.update_date.desc(), ProjectProgress.update_time.desc()).all()

    result = []
    for update in updates:
        project = Project.query.get(update.project_id)
        user = User.query.get(update.updated_by)
        if project and not project.is_deleted:
            result.append({
                'id': update.id,
                'project_id': update.project_id,
                'project_name': project.name,
                'client_name': project.client_name,
                'project_stage': project.stage,
                'project_stage_text': STAGE_MAP.get(project.stage, str(project.stage)),
                'update_content': update.update_content,
                'update_date': str(update.update_date),
                'update_time': str(update.update_time),
                'updated_by': user.username if user else '未知用户',
                'is_important': update.is_important
            })

    return jsonify({
        'success': True,
        'message': '获取成功',
        'data': result,
        'count': len(result),
        'time_range': {
            'start_date': str(first_day_of_month),
            'end_date': str(today)
        }
    })


@bp.route('/range-updates', methods=['GET'])
def get_range_updates():
    """获取指定日期范围内的全部项目更新记录（公开接口）
    
    Query参数:
        start_date: 开始日期 (YYYY-MM-DD)
        end_date:   结束日期 (YYYY-MM-DD)
    """
    from flask import request

    start_date_str = request.args.get('start_date')
    end_date_str = request.args.get('end_date')

    if not start_date_str or not end_date_str:
        return jsonify({
            'success': False,
            'message': '缺少必要参数: start_date 和 end_date 均为必填项'
        }), 400

    try:
        start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
        end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
    except ValueError:
        return jsonify({
            'success': False,
            'message': '日期格式错误，请使用 YYYY-MM-DD 格式'
        }), 400

    if start_date > end_date:
        return jsonify({
            'success': False,
            'message': 'start_date 不能晚于 end_date'
        }), 400

    updates = ProjectProgress.query.filter(
        ProjectProgress.update_date >= start_date,
        ProjectProgress.update_date <= end_date
    ).order_by(ProjectProgress.update_date.desc(), ProjectProgress.update_time.desc()).all()

    result = []
    for update in updates:
        project = Project.query.get(update.project_id)
        user = User.query.get(update.updated_by)
        if project and not project.is_deleted:
            result.append({
                'id': update.id,
                'project_id': update.project_id,
                'project_name': project.name,
                'client_name': project.client_name,
                'project_stage': project.stage,
                'project_stage_text': STAGE_MAP.get(project.stage, str(project.stage)),
                'update_content': update.update_content,
                'update_date': str(update.update_date),
                'update_time': str(update.update_time),
                'updated_by': user.username if user else '未知用户',
                'is_important': update.is_important
            })

    return jsonify({
        'success': True,
        'message': '获取成功',
        'data': result,
        'count': len(result),
        'time_range': {
            'start_date': str(start_date),
            'end_date': str(end_date)
        }
    })
