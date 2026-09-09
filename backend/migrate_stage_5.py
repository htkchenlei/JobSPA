"""把项目阶段从 1-13 档迁移/归一化为 5 档：
  1 立项中  2 已立项  3 招投标  4 已中标  5 已完成

旧映射：
  1-2   -> 1（立项中）
  3-5   -> 2（已立项）
  6-8   -> 3（招投标）
  9-11  -> 4（已中标）
  12-13 -> 5（已完成）

幂等：执行后阶段只会是 1..5。建议先备份数据库：
  cp data/projectmanagement.db data/projectmanagement.db.bak
"""
import sqlite3

DB_PATH = 'projectmanagement.db'
con = sqlite3.connect(DB_PATH)
cur = con.cursor()

cur.execute("SELECT id, stage FROM projects ORDER BY id")
rows = cur.fetchall()
print(f'项目总数: {len(rows)}')

changed = 0
for pid, old in rows:
    if old is None:
        continue
    try:
        old = int(old)
    except (TypeError, ValueError):
        continue
    if old <= 0 or old > 13:
        continue
    new = old
    if old <= 2:
        new = 1
    elif old <= 5:
        new = 2
    elif old <= 8:
        new = 3
    elif old <= 11:
        new = 4
    else:
        new = 5
    if new != old:
        cur.execute("UPDATE projects SET stage = ? WHERE id = ?", (new, pid))
        changed += 1

con.commit()
print(f'已迁移 {changed} 个项目')
cur.execute("SELECT stage, COUNT(*) FROM projects GROUP BY stage ORDER BY stage")
print('迁移后阶段分布:')
for r in cur.fetchall():
    print('  stage', r[0], '=', r[1])
con.close()
