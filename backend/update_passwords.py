from app import app, db
from app.models.models import User
from werkzeug.security import generate_password_hash

# 默认密码
DEFAULT_PASSWORD = "tianyu.123"

with app.app_context():
    try:
        # 获取所有用户
        users = User.query.all()
        
        # 生成密码哈希
        password_hash = generate_password_hash(DEFAULT_PASSWORD)
        
        # 更新所有用户的密码
        for user in users:
            user.password = password_hash
            db.session.add(user)
        
        # 提交更改
        db.session.commit()
        
        print(f"成功更新了 {len(users)} 个用户的密码为: {DEFAULT_PASSWORD}")
        print("密码已加密存储到数据库中")
        
    except Exception as e:
        print(f"更新密码失败: {str(e)}")
        db.session.rollback()
    finally:
        db.session.close()
