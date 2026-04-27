from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime, Date, Time, Enum
from sqlalchemy.orm import relationship
from happ import db, app
from flask_login import UserMixin
from enum import Enum as UserEnum
from datetime import datetime



class UserRole(UserEnum):
    ADMIN = 1
    PATIENT = 2


#1. Trạng thái lịch hẹn
class AppointmentStatus(UserEnum):
    CONFIRMED = 1    #Đã xác nhận
    COMPLETED = 2    #Đã khám
    CANCELLED = 3    #Đã hủy


class BaseModel(db.Model):
    __abstract__ = True
    id = Column(Integer, primary_key=True, autoincrement=True)
    active = Column(Boolean, default=True)



#2. Bảng Người dùng (Admin và Bệnh nhân)
class User(BaseModel, UserMixin):
    # __tablename__ = 'user'
    name = Column(String(100), nullable=False)
    username = Column(String(50), nullable=False, unique=True)
    password = Column(String(100), nullable=False)
    avatar = Column(String(255), default='https://res.cloudinary.com/dref2n2l6/image/upload/v1777218869/q11worsfftrglsarueqn.png')
    user_role = Column(Enum(UserRole), default=UserRole.PATIENT)

    # Một bệnh nhân có nhiều lịch hẹn
    appointments = relationship('Appointment', backref='patient', lazy=True)

    def __str__(self):
        return self.name


#3. Bảng Bác sĩ (Chỉ lưu thông tin bác sĩ để bệnh nhân chọn)
class Doctor(BaseModel):
    # __tablename__ = 'doctor'
    name = Column(String(100), nullable=False)
    specialty = Column(String(100))  # Gõ tay chuyên khoa trực tiếp vào đây
    description = Column(String(255))

    # Một bác sĩ có nhiều lịch hẹn
    appointments = relationship('Appointment', backref='doctor', lazy=True)

    def __str__(self):
        return self.name




#4. Bảng Lịch hẹn
class Appointment(BaseModel):
    __tablename__ = 'appointment'
    patient_id = Column(Integer, ForeignKey(User.id), nullable=False)
    doctor_id = Column(Integer, ForeignKey(Doctor.id), nullable=False)

    app_date = Column(Date, nullable=False)  # Ngày hẹn khám
    slot_time = Column(Time, nullable=False)  # Giờ khám (Cách nhau 15p: 08:00, 08:15...)

    status = Column(Enum(AppointmentStatus), default=AppointmentStatus.CONFIRMED)
    created_date = Column(DateTime, default=datetime.now)

if __name__ == '__main__':
    with app.app_context():
        db.drop_all()
        db.create_all()
        import hashlib

        # 1. Tạo Admin mẫu (nếu chưa có)
        if not User.query.filter_by(username='admin').first():
            password_hashed = str(hashlib.md5('123456'.encode('utf-8')).hexdigest())
            admin = User(name='Admin', username='admin',
                         password=password_hashed, user_role=UserRole.ADMIN)
            db.session.add(admin)

        # 2. Tạo Bệnh nhân mẫu (Để 2 người cùng có tài khoản test)
        if not User.query.filter_by(user_role=UserRole.PATIENT).first():
            p_pass = str(hashlib.md5('123456'.encode('utf-8')).hexdigest())
            p1 = User(name='Nguyễn Văn An', username='patient01',
                      password=p_pass, user_role=UserRole.PATIENT)
            p2 = User(name='Lê Thị Lam', username='patient02',
                      password=p_pass, user_role=UserRole.PATIENT)
            db.session.add_all([p1, p2])

        # 3. Tạo Bác sĩ mẫu
        if not Doctor.query.first():
            d1 = Doctor(name='BS. Đào Thanh Hải', specialty='Nội khoa')
            d2 = Doctor(name='BS. Trần Chính', specialty='Nhi khoa')
            d3 = Doctor(name='BS. Lê Linh Thi', specialty='Nhi khoa')
            db.session.add_all([d1, d2, d3])

        db.session.commit()  # Lưu tất cả vào MySQL
        print("Đã tạo Database thành công!")

