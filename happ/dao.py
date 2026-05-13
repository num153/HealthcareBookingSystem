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


from datetime import datetime, timedelta
from happ.models import Appointment, AppointmentStatus, db

#Logic huỷ lịch
def cancel_appointment(appointment_id, current_user_id):
    # 1. Tìm lịch hẹn
    app = Appointment.query.get(appointment_id)
    if not app:
        return False, "Không tìm thấy lịch hẹn."

    # 2. Ràng buộc: Chỉ bệnh nhân đặt lịch (hoặc admin sau này) mới được hủy
    if app.patient_id != current_user_id:
        return False, "Bạn không có quyền hủy lịch của người khác."

    # 3. Ràng buộc: Không được hủy nếu trạng thái là COMPLETED
    if app.status == AppointmentStatus.COMPLETED:
        return False, "Không thể hủy lịch đã khám xong."

    # 4. Ràng buộc: Không được hủy khi còn dưới 1 giờ trước giờ khám
    # Ghép ngày và giờ khám lại thành 1 object datetime
    appointment_datetime = datetime.combine(app.app_date, app.slot_time)
    time_difference = appointment_datetime - datetime.now()

    if time_difference < timedelta(hours=1):
        return False, "Chỉ được hủy lịch trước giờ khám ít nhất 1 tiếng."

    #Nếu pass được hết --> cho phép huỷ

    # Đổi trạng thái thành CANCELLED
    app.status = AppointmentStatus.CANCELLED

    # Ràng buộc: Xử lý vụ hủy quá 3 lần/tuần
    user = app.patient
    user.cancel_count += 1

    if user.cancel_count >= 3:
        # Phạt hạn chế đặt lịch trong 24 giờ
        user.restricted_until = datetime.now() + timedelta(hours=24)
        # Có thể reset lại cancel_count về 0 ở đây nếu muốn bắt đầu chu kỳ mới, tùy logic nhóm bạn.

    try:
        db.session.commit()
        return True, "Hủy lịch thành công!"
    except Exception as e:
        db.session.rollback()
        return False, str(e)