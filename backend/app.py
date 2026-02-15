# 导入app包中的应用实例
from app import app

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=15667)