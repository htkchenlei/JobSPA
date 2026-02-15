# 导入app包中的应用实例
from app import app
import os

# 打印当前工作目录和数据库连接字符串
print(f"当前工作目录: {os.getcwd()}")
print(f"数据库连接字符串: {app.config['SQLALCHEMY_DATABASE_URI']}")

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)