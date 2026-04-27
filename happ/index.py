from flask import render_template, request, redirect, url_for
from flask_login import login_user, logout_user
from happ import app, login
from happ.models import User, UserRole
from happ import dao
import hashlib


def register_routes(app):
    @app.route("/")
    def index():
        return "Chào mừng bạn đến với trang chủ đặt lịch khám!"



    @app.route('/login', methods=['get', 'post'])
    def login_view():
        err_msg = ""
        if request.method == 'POST':
            username = request.form.get('username')
            password = request.form.get('password')

            # Gọi dao để kiểm tra database
            user = dao.auth_user(username=username, password=password)

            if user:
                login_user(user=user)

                # KIỂM TRA ROLE ĐỂ ĐIỀU HƯỚNG
                if user.user_role == UserRole.ADMIN:
                    return redirect('/admin')  # Trang mặc định của Flask-Admin
                else:
                    return redirect(url_for('index'))  # Trang chủ dành cho Patient
            else:
                err_msg = "Tên đăng nhập hoặc mật khẩu không chính xác!"

        return render_template('layout/login.html', err_msg=err_msg)


@login.user_loader
def load_user(user_id):
    from happ.models import User
    return User.query.get(int(user_id))

if __name__ == '__main__':
    register_routes(app)
    app.run(debug=True)