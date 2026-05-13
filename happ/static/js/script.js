function cancelApp(btn) {
    const appId = btn.getAttribute('data-id');

    if(confirm('Bạn có chắc chắn muốn hủy lịch hẹn này không?')) {
        fetch(`/api/cancel-appointment/${appId}`, {
            method: 'POST'
        })
        .then(res => res.json())
        .then(data => {
            if(data.status === 'success') {
                alert(data.message);
                location.reload(); // Load lại trang để cập nhật trạng thái
            } else {
                alert('Lỗi: ' + data.message);
            }
        })
        .catch(err => console.error(err));
    }
}
