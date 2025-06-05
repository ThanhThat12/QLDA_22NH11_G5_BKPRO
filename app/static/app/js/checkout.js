    document.addEventListener('DOMContentLoaded', function() {
        const form = document.querySelector('form');
        const shippingRadios = document.querySelectorAll('input[name="ShippingMethod"]');
        const paymentRadios = document.querySelectorAll('input[name="payment"]');
        const finalTotalElement = document.getElementById('final-total');
        const subtotalElement = document.getElementById('checkout-subtotal');
        const popupTotalElement = document.getElementById('popup-total'); // Thêm dòng này
        
        // Lấy giá trị tổng phụ ban đầu từ thuộc tính dữ liệu
        const subtotal = parseFloat(subtotalElement.getAttribute('data-value'));

        // Chức năng cập nhật tổng số dựa trên vận chuyển đã chọn
        function updateTotal() {
            const selectedShipping = document.querySelector('input[name="ShippingMethod"]:checked');
            let shippingCost = 0;
            
            if (selectedShipping) {
                shippingCost = parseFloat(selectedShipping.value);
            }
            
            const newTotal = subtotal + shippingCost;
            finalTotalElement.textContent = `$${newTotal.toFixed(2)}`;
            // if (popupTotalElement) {
            // popupTotalElement.textContent = `Total: $${newTotal.toFixed(2)}`; // Cập nhật popup
            // }
        }

        // Thêm trình lắng nghe sự kiện vào nút radio vận chuyển
        shippingRadios.forEach(radio => {
            radio.addEventListener('change', updateTotal);
        });

         
    });

    document.addEventListener('DOMContentLoaded', function() {
        const form = document.getElementById('checkout-form'); // Đảm bảo form có id này
        const popupTotalElement = document.getElementById('popup-total');
        const finalTotalElement = document.getElementById('final-total');

        form.addEventListener('submit', function(e) {
            e.preventDefault(); // Quan trọng: ngừng submit mặc định
            
            const selectedShipping = document.querySelector('input[name="ShippingMethod"]:checked');
            const selectedPayment = document.querySelector('input[name="payment"]:checked');

            // Kiểm tra phương thức vận chuyển
            if (!selectedShipping) {
                Swal.fire({
                    icon: 'warning',
                    iconColor: '#81c408',
                    title: 'Oops...',
                    text: 'Please select a shipping method!',
                    confirmButtonColor: '#d33',
                });
                return false; // Dừng xử lý
            }

            // Kiểm tra phương thức thanh toán
            if (!selectedPayment) {
                Swal.fire({
                    icon: 'warning',
                    iconColor: '#81c408',
                    title: 'Oops...',
                    text: 'Please select a payment method!',
                    confirmButtonColor: '#81c408',
                });
                return false;
            }

            // Nếu chọn phương thức thanh toán là "online"
            if (selectedPayment.value === 'online') {
                // Hiển thị popup thanh toán trực tuyến
                if (popupTotalElement && finalTotalElement) {
                popupTotalElement.textContent = `Total: ${finalTotalElement.textContent}`; // Đồng bộ giá trị
                }
                $('#paymentPopup').modal('show');
                return false; // Ngừng submit và chỉ hiển thị popup
            }

            // Nếu đã chọn đủ, hiển thị xác nhận
            Swal.fire({
                title: 'Are you sure?',
                text: "You're about to place your order!",
                icon: 'question',
                showCancelButton: true,
                confirmButtonColor: '#81c408',
                cancelButtonColor: '#d33',
                confirmButtonText: 'Yes, place order!'
            }).then((result) => {
                if (result.isConfirmed) {
                    // Chỉ submit khi người dùng xác nhận
                    form.submit();
                }
            });
        });

        // Lắng nghe sự kiện khi người dùng nhấn nút "Confirm" trong popup
        document.getElementById('confirmPayment').addEventListener('click', function() {
            form.submit();  // Gửi form khi người dùng xác nhận thanh toán
        });

        // Lắng nghe sự kiện khi người dùng nhấn nút "Cancel" trong popup
        document.getElementById('cancelPayment').addEventListener('click', function() {
            $('#paymentPopup').modal('hide');  // Đóng popup
        });
    });
