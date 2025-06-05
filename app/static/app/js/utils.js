function showLoginPopup() {
    Swal.fire({
        icon: 'warning',
        title: 'Bạn chưa đăng nhập',
        text: 'Vui lòng đăng nhập để thêm sản phẩm vào giỏ hàng.',
        confirmButtonText: 'Đăng nhập',
        showCancelButton: true,
        cancelButtonText: 'Hủy'
    }).then((result) => {
        if (result.isConfirmed) {
            window.location.href = '/loginregister/';
        }
    });
}

function showErrorPopup(errorMessage) {
    Swal.fire({
        icon: 'error',
        title: 'Lỗi',
        text: errorMessage,
        confirmButtonText: 'OK'
    });
}