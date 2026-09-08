"""补齐 work_log 表：把 project_progress 中有数据但 work_log 中没有记录的日期同步过去。

- 已存在 AI 日志的日期会被跳过，不覆盖。
- 新增记录的 work_log_by_ai 由项目进展拼装，非空，这样前端日历 hasLog 也会正确标记。
- user 字段取当天出现次数最多的项目所有者用户名对应的用户 ID，兜底为 admin。
- 幂等：重复运行只跳过已有日期。
"""
import sqlite3
from collections import Counter
from datetime import time as dtime

DB_PATH = 'projectmanagement.db'
con = sqlite3.connect(DB_PATH)
cur = con.cursor()

cur.execute("SELECT id, username FROM users")
user_map = {name: uid for uid, name in cur.fetchall()}
print('users:', user_map)

cur.execute(
    """
    SELECT pp.update_date, pp.update_time, p.id, p.owner, pp.update_content
    FROM project_progress pp
    JOIN projects p ON pp.project_id = p.id
    ORDER BY pp.update_date, pp.update_time
    """
)
rows = cur.fetchall()
print('progress rows:', len(rows))

daily = {}
for date, t, pid, owner, content in rows:
    if date not in daily:
        daily[date] = {'items': [], 'owners': [], 'last_time': None}
    daily[date]['items'].append((pid, content))
    daily[date]['owners'].append(owner)
    if t and (not daily[date]['last_time'] or str(t) > str(daily[date]['last_time'])):
        daily[date]['last_time'] = t

print('unique dates with progress:', len(daily))

inserted = 0
skipped = 0
failed = 0
for date, info in daily.items():
    cur.execute("SELECT COUNT(*) FROM work_log WHERE log_date = ?", (date,))
    if cur.fetchone()[0] > 0:
        skipped += 1
        continue
    cnt = Counter([o for o in info['owners'] if o])
    owner = cnt.most_common(1)[0][0] if cnt else None
    user_id = user_map.get(owner, 1)

    items_text = '\n'.join(f"[项目 #{pid}] {content}" for pid, content in info['items'])
    summary = (
        f"【系统补齐 · 来源：项目进展】今日共 {len(info['items'])} 项项目进展。\n{items_text}"
    )
    last_time = info['last_time'] or dtime(0, 0, 0)
    try:
        cur.execute(
            """
            INSERT INTO work_log (today_activities, user, work_log_by_ai, log_date, log_time, created_by_ai)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (items_text, user_id, summary, date, last_time, '系统补齐'),
        )
        inserted += 1
    except Exception as e:
        failed += 1
        print(f'fail {date}: {e}')

con.commit()

cur.execute("SELECT substr(log_date,1,7) ym, COUNT(*) FROM work_log GROUP BY ym ORDER BY ym")
print('work_log after sync by month:')
for r in cur.fetchall():
    print(' ', r)
print(f'inserted={inserted}, skipped_existing={skipped}, failed={failed}')