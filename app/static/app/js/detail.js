// document.addEventListener('DOMContentLoaded', function () {
//     // Lấy user và csrftoken từ template hoặc DOM
//     const user = "{{ request.user.username|default:'AnonymousUser' }}"; // Cần truyền từ template
//     const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]')?.value || getCookie('csrftoken');

//     if (!csrftoken) {
//         console.error('CSRF token not found');
//         showErrorPopup('Không tìm thấy CSRF token. Vui lòng thử lại.');
//         return;
//     }

//     const updateCartButtons = document.getElementsByClassName('update-cart-detail');

//     for (let button of updateCartButtons) {
//         button.addEventListener('click', function () {
//             const productId = this.dataset.product;
//             const action = this.dataset.action;
//             const quantityInput = this.closest('.input-group')?.querySelector('.quantity-input');
//             let quantity = quantityInput ? parseInt(quantityInput.value) : 1;

//             if (isNaN(quantity) || quantity < 1) {
//                 showErrorPopup('Vui lòng nhập số lượng hợp lệ.');
//                 return;
//             }

//             if (user === 'AnonymousUser') {
//                 showLoginPopup();
//             } else if (action === 'add-cart-detail') {
//                 addToCart(productId, action, quantity);
//             }
//         });
//     }

//     function addToCart(productId, action, quantity) {
//         Swal.fire({
//             title: 'Đang xử lý...',
//             allowOutsideClick: false,
//             didOpen: () => Swal.showLoading()
//         });

//         fetch('/update_item_detail/', {
//             method: 'POST',
//             headers: {
//                 'Content-Type': 'application/json',
//                 'X-CSRFToken': csrftoken,
//             },
//             body: JSON.stringify({ productId, action, quantity })
//         })
//         .then(response => response.json())
//         .then(data => {
//             Swal.close();
//             if (data.error) {
//                 if (data.error.includes('đăng nhập')) {
//                     showLoginPopup();
//                 } else {
//                     showErrorPopup(data.error);
//                 }
//             } else {
//                 updateCartCount();
//                 Swal.fire({
//                     title: 'Success!',
//                     text: `Product has been added to the cart.`,
//                     icon: 'success',
//                     confirmButtonText: 'OK'
//                 });
//             }
//         })
//         .catch(error => {
//             Swal.close();
//             showErrorPopup('Đã có lỗi xảy ra. Vui lòng thử lại.');
//             console.error('Error:', error);
//         });
//     }

//     function updateCartCount() {
//         fetch('/get_cart_count/')
//         .then(response => response.json())
//         .then(data => {
//             const cartCount = document.getElementById('cart-count');
//             if (cartCount) {
//                 cartCount.textContent = data.cartItems || 0;
//             }
//         })
//         .catch(error => console.error('Error updating cart count:', error));
//     }

//     // Hàm lấy CSRF token từ cookie (nếu không dùng input ẩn)
//     function getCookie(name) {
//         let cookieValue = null;
//         if (document.cookie && document.cookie !== '') {
//             const cookies = document.cookie.split(';');
//             for (let i = 0; i < cookies.length; i++) {
//                 const cookie = cookies[i].trim();
//                 if (cookie.substring(0, name.length + 1) === (name + '=')) {
//                     cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
//                     break;
//                 }
//             }
//         }
//         return cookieValue;
//     }
// });


   // Xử lý sự kiện click nút "Add to cart"
    const updateCartButtons = document.getElementsByClassName('update-cart-detail');
    
    for (let i = 0; i < updateCartButtons.length; i++) {
        updateCartButtons[i].addEventListener('click', function() {
            const productId = this.dataset.product;
            const action = this.dataset.action;
            
            const quantityInput = this.closest('.mb-5').querySelector('.quantity-input');
            let quantity = quantityInput ? parseInt(quantityInput.value) : 1;

            console.log('productId:', productId, 'Action:', action, 'Quantity:', quantity);
            console.log('USER:', user);

            if (isNaN(quantity) || quantity < 1) {
                showErrorPopup('Vui lòng nhập số lượng hợp lệ.');
                return;
            }

            // Kiểm tra đăng nhập
            if (typeof user === 'undefined' || user === 'AnonymousUser') {
                showLoginPopup();
            } else {
                
                if (action === 'add-cart-detail') {
                    addToCart(productId, action,quantity);
                }
            }
        });
    }


    function addToCart(productId,action, quantity) {
        if (quantity < 1) {
            quantity = 1;
        }
        
            fetch('/update_item_detail/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrftoken,
                },
                body: JSON.stringify({ 'productId': productId, 'action': action, 'quantity': quantity })
            })
            .then(response => response.json())
            .then(data => {
                console.log('data:', data);
                updateCartCount();

            
            Swal.fire({
            title: 'Thành công!',
            text: 'Sản phẩm đã được thêm vào giỏ hàng.',
            icon: 'success',
            confirmButtonText: 'OK'
        });
                
            })
            .catch(error => console.error('Error:', error));
        
    }


    function updateCartCount() {
        fetch('/get_cart_count/')  
        .then(response => response.json())
        .then(data => {
            document.getElementById('cart-count').textContent = data.cartItems; 
            
        })
        .catch(error => console.error('Error updating cart count:', error));
    }