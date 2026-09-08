"""每月“有项目进展的日期”缓存。

用途：工作日志页日历需要知道当月哪些天有项目进展来渲染颜色标记。
为避免每次进入页面都按“天”查询数据库，这里把结果缓存为 JSON 文件；
当用户新增项目进展（写日志）时同步更新该文件。

文件位置：与 SQLite 数据库同一目录，文件名 progress_days_cache.json。
结构示例：
{
  "2026-09": {
    "days": [1, 4, 7],
    "counts": {"1": 1, "4": 2, "7": 2},
    "refreshed": "2026-09-08"
  }
}
"""
import json
import os
import threading
from datetime import date

from sqlalchemy.engine.url import make_url

_LOCK = threading.Lock()


def cache_path(app):
    uri = app.config.get('SQLALCHEMY_DATABASE_URI', '')
    db_dir = '.'
    try:
        url = make_url(uri)
        if getattr(url, 'database', None):
            db_dir = os.path.dirname(os.path.abspath(url.database))
    except Exception:
        db_dir = '.'
    if db_dir and not os.path.isdir(db_dir):
        try:
            os.makedirs(db_dir, exist_ok=True)
        except Exception:
            pass
    return os.path.join(db_dir, 'progress_days_cache.json')


def _read(app):
    path = cache_path(app)
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError, OSError):
        return {}


def _write(app, data):
    path = cache_path(app)
    tmp = path + '.tmp'
    try:
        with open(tmp, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False)
        os.replace(tmp, path)
    except Exception as e:
        print(f"写入缓存文件失败: {e}")


def get_month_entry(app, year, month):
    """返回缓存中某月的记录 dict；无缓存或缓存非当天刷新时返回 None（需重建）。"""
    key = f"{year:04d}-{month:02d}"
    today_str = date.today().isoformat()
    with _LOCK:
        data = _read(app)
        entry = data.get(key)
        if not entry:
            return None
        if entry.get('refreshed') != today_str:
            return None
        return entry


def set_month_days(app, year, month, items):
    """写缓存。items: [{day: int, count: int}, ...]"""
    key = f"{year:04d}-{month:02d}"
    days = sorted(d['day'] for d in items)
    counts = {str(d['day']): d['count'] for d in items}
    entry = {'days': days, 'counts': counts, 'refreshed': date.today().isoformat()}
    with _LOCK:
        data = _read(app)
        data[key] = entry
        _write(app, data)


def add_day(app, year, month, day):
    """新增一条项目进展后调用：把当天计入缓存。若该月尚未缓存则忽略（下次访问重建）。"""
    key = f"{year:04d}-{month:02d}"
    today_str = date.today().isoformat()
    with _LOCK:
        data = _read(app)
        entry = data.get(key)
        if not entry:
            return
        days = entry.get('days') or []
        counts = entry.get('counts') or {}
        if day not in days:
            days.append(day)
            days.sort()
        counts[str(day)] = int(counts.get(str(day), 0)) + 1
        entry['days'] = days
        entry['counts'] = counts
        entry['refreshed'] = today_str
        data[key] = entry
        _write(app, data)
