import sqlite3
conn = sqlite3.connect('projectmanagement.db')
cursor = conn.execute('SELECT id, username, password FROM users')
users = cursor.fetchall()
for user in users:
    print(f'User: {user[1]}, Password: {user[2]}')
conn.close()
