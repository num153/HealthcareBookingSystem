# HealthcareBookingSystem
# HỆ THỐNG QUẢN LÝ ĐẶT LỊCH KHÁM BỆNH

## 1. Giới thiệu

Đây là dự án xây dựng hệ thống quản lý đặt lịch khám bệnh, phục vụ cho bài tập lớn môn Kiểm thử phần mềm.
Hệ thống cho phép bệnh nhân đặt lịch khám với bác sĩ tại phòng khám, đồng thời đảm bảo các ràng buộc nghiệp vụ được kiểm soát chặt chẽ.

---

## 2. Mục tiêu

* Xây dựng hệ thống đặt lịch khám cơ bản
* Áp dụng các kỹ thuật kiểm thử phần mềm
* Đảm bảo tính đúng đắn của các ràng buộc nghiệp vụ

---

## 3. Công nghệ sử dụng

* Python (Flask)
* MySQL
* Git và GitHub

---

## 4. Chức năng chính

### 4.1. Đặt lịch khám

Cho phép bệnh nhân đặt lịch khám với bác sĩ.

Ràng buộc:

* Người dùng phải đăng nhập
* Chỉ được đặt lịch trong giờ làm việc (8:00 - 17:00)
* Không được đặt lịch trong quá khứ
* Mỗi khung giờ chỉ có 1 bệnh nhân
* Mỗi bệnh nhân tối đa 2 lịch mỗi ngày
* Không được đặt lịch nếu bác sĩ đang nghỉ phép
* Không được đặt lịch quá 30 ngày trong tương lai

---

### 4.2. Hủy lịch khám

Cho phép bệnh nhân hoặc admin hủy lịch khám.

Ràng buộc:

* Chỉ bệnh nhân đã đặt lịch hoặc admin mới được hủy
* Không được hủy nếu còn dưới 1 giờ trước giờ khám
* Không được hủy nếu trạng thái lịch là Completed
* Nếu hủy quá 3 lần trong tuần, tài khoản bị hạn chế đặt lịch trong 24 giờ

---

### 4.3. Quản lý lịch bác sĩ

Cho phép admin quản lý lịch làm việc của bác sĩ.

Ràng buộc:

* Chỉ admin mới được tạo lịch làm việc
* Mỗi bác sĩ tối đa 20 lịch khám mỗi ngày
* Không được tạo lịch trùng thời gian


## 5. Định hướng phát triển

* Xây dựng giao diện người dùng
* Thêm xác thực và phân quyền chi tiết
* Tích hợp thông báo (email hoặc SMS)
* Mở rộng API

