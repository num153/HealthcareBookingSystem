from datetime import datetime, date, time, timedelta


def is_working_hour(appt_time):
    """Ràng buộc: chỉ đặt lịch trong giờ làm việc 8:00–17:00."""
    return time(8, 0) <= appt_time <= time(17, 0)


def is_future_datetime(appt_date, appt_time):
    """Ràng buộc: không đặt lịch trong quá khứ."""
    appt_dt = datetime.combine(appt_date, appt_time)
    return appt_dt > datetime.now()


def is_within_30_days(appt_date):
    """Ràng buộc: không đặt quá 30 ngày trong tương lai."""
    return 0 <= (appt_date - date.today()).days <= 30


def format_date(d):
    """Định dạng ngày hiển thị: 12/05/2026."""
    if d:
        return d.strftime('%d/%m/%Y')
    return ''


def format_time(t):
    """Định dạng giờ hiển thị: 08:30."""
    if t:
        return t.strftime('%H:%M')
    return ''


def can_cancel_appointment(appointment):
    """
    Kiểm tra lịch khám có thể huỷ không.
    Trả về (True/False, thông báo lỗi nếu có).
    """
    if appointment.status == 'Completed':
        return False, 'Không thể huỷ lịch đã hoàn thành.'

    if appointment.status == 'Cancelled':
        return False, 'Lịch này đã được huỷ trước đó.'

    appt_dt = datetime.combine(appointment.app_date, appointment.slot_time)
    if (appt_dt - datetime.now()) < timedelta(hours=1):
        return False, 'Không thể huỷ lịch trong vòng 1 giờ trước giờ khám.'

    return True, None