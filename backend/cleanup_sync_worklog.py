"""清理“系统补齐”占位工作日志。

背景：早期为了给工作日志日历“补日期颜色”，曾把 project_progress 自动补齐成 work_log 占位记录。
产品规则为：工作日志只在用户手动点击“生成今日日志”并保存时才产生，不做自动生成/补齐。

本脚本删除 created_by_ai = '系统补齐' 的记录；真正手动生成（AI）的工作日志不受影响。
日历颜色不受影响：颜色仍来自 project_progress（month-days 缓存），该表数据不动。

建议执行前先备份数据库：
  cp data/projectmanagement.db data/projectmanagement.db.bak

运行（在项目根/后端目录，确保 DATABASE_URL 指向目标库）：
  python cleanup_sync_worklog.py
"""
import sqlite3

DB_PATH = 'projectmanagement.db'
con = sqlite3.connect(DB_PATH)
cur = con.cursor()

cur.execute("SELECT COUNT(*) FROM work_log WHERE created_by_ai = '系统补齐'")
n = cur.fetchone()[0]
print(f'待清理的“系统补齐”记录数: {n}')

cur.execute("DELETE FROM work_log WHERE created_by_ai = '系统补齐'")
con.commit()
print(f'已删除 {cur.rowcount} 条记录')

cur.execute("SELECT COUNT(*) FROM work_log")
print(f'剩余工作日志总数: {cur.fetchone()[0]}')
con.close()
