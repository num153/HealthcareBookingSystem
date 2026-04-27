from sqlalchemy.exc import IntegrityError
from happ.models import User
import hashlib
from happ import app, db
import cloudinary.uploader
from flask_login import current_user
from sqlalchemy import func
from datetime import datetime

# 1. Hàm lấy thông tin User bằng ID
# Phục vụ cho Flask-Login duy trì phiên đăng nhập (session)
def get_user_by_id(user_id):
    return User.query.get(user_id)


# 2. Hàm xác thực tài khoản (Authentication)
# Dùng để kiểm tra khi người dùng bấm nút "Đăng nhập"
def auth_user(username, password):
    if username and password:
        # Mã hóa MD5 mật khẩu người dùng nhập vào để so khớp với DB
        password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())

        # Tìm user có username và password khớp hoàn toàn
        return User.query.filter(User.username.__eq__(username.strip()),
                                 User.password.__eq__(password)).first()
    return None


# 3. Hàm lấy vai trò của User (Nếu cần dùng thêm logic ở index)
def get_user_role(user):
    if user:
        return user.user_role
    return None