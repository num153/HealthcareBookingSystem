from flask import render_template, request, redirect, url_for, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from happ import app, login, admin
from happ.models import User, UserRole
from happ import dao
import hashlib
from happ.models import Appointment


def register_routes(app):
    @app.route("/")
    def index():
        return render_template('index.html')

    @app.route("/dashboard")
    @login_required
    def dashboard():
        # Lấy tất cả lịch hẹn của user hiện tại, sắp xếp theo ngày gần nhất
        appointments = Appointment.query.filter_by(patient_id=current_user.id).order_by(
        Appointment.app_date.desc()).all()
        return render_template('dashboard.html',appointments=appointments)

    @app.route('/register', methods=['get', 'post'])
    def register_view():
        return render_template('layout/register.html')

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

                # --- Lấy đường link cũ mà người dùng muốn vào (nếu có) ---
                next_page = request.args.get('next')

                # KIỂM TRA ROLE ĐỂ ĐIỀU HƯỚNG
                if user.user_role == UserRole.ADMIN:
                    # Nếu có link cũ (next_page) thì ưu tiên về link đó, không thì về /admin
                    return redirect(next_page if next_page else '/admin')
                else:
                    # Nếu có link cũ thì ưu tiên về link đó, không thì về trang chủ
                    return redirect(next_page if next_page else url_for('index'))
            else:
                err_msg = "Tên đăng nhập hoặc mật khẩu không chính xác!"

        return render_template('layout/login.html', err_msg=err_msg)

    # === THÊM ROUTE ĐĂNG XUẤT Ở ĐÂY ===
    @app.route('/logout')
    @login_required # Chỉ ai đăng nhập rồi mới được đăng xuất
    def logout():
        logout_user() # Xóa session
        return redirect(url_for('index')) # Đá về trang chủ

    # === THÊM ROUTE HỦY LỊCH Ở ĐÂY ===
    @app.route('/api/cancel-appointment/<int:app_id>', methods=['POST'])
    @login_required  # Bắt buộc phải đăng nhập mới được gọi
    def api_cancel_appointment(app_id):
        # Gọi hàm dao xử lý hủy
        success, message = dao.cancel_appointment(app_id, current_user.id)

        if success:
            return jsonify({'status': 'success', 'message': message})
        else:
            return jsonify({'status': 'error', 'message': message}), 400


# === CẤU HÌNH FLASK-LOGIN CHO VIỆC CHƯA ĐĂNG NHẬP ===
login.login_view = 'login_view' # Chỉ định hàm xử lý trang đăng nhập
login.login_message = "Hãy đăng nhập để thực hiện hành động này." # Thông báo hiện ra khi bị đá về login

@login.user_loader
def load_user(user_id):
    from happ.models import User
    return User.query.get(int(user_id))


if __name__ == '__main__':
    register_routes(app)
    app.run(debug=True)