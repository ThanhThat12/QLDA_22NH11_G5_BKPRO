document.addEventListener('DOMContentLoaded', function() {
    // // Tab switching functionality
    // const tabs = document.querySelectorAll('.account-nav li');
    // const contentSections = document.querySelectorAll('.account-tab');
    
    // tabs.forEach(tab => {
    //     tab.addEventListener('click', function() {
    //         const tabId = this.getAttribute('data-tab');
            
    //         // Remove active class from all tabs and content sections
    //         tabs.forEach(t => t.classList.remove('active'));
    //         contentSections.forEach(section => section.classList.remove('active'));
            
    //         // Add active class to current tab and content section
    //         this.classList.add('active');
    //         document.getElementById(tabId).classList.add('active');
    //     });
    // });

    // const tabs = document.querySelectorAll('.account-nav li');
    // const contentSections = document.querySelectorAll('.account-tab');
    
    // // Function to activate tab based on ID without scrolling
    // function activateTab(tabId) {
    //     // Remove active class from all tabs and content sections
    //     tabs.forEach(t => t.classList.remove('active'));
    //     contentSections.forEach(section => section.classList.remove('active'));
        
    //     // Add active class to current tab and content section
    //     const currentTab = document.querySelector(`.account-nav li[data-tab="${tabId}"]`);
    //     if (currentTab) {
    //         currentTab.classList.add('active');
    //         const contentSection = document.getElementById(tabId);
    //         if (contentSection) {
    //             contentSection.classList.add('active');
    //         }
    //     }
    // }
    
    // // Check URL hash on page load without scrolling
    // function checkHash() {
    //     let hash = window.location.hash.substring(1); // Remove the # symbol
    //     if (hash && document.getElementById(hash)) {
    //         activateTab(hash);
    //         // Prevent scrolling to element
    //         setTimeout(function() {
    //             window.scrollTo(0, 0);
    //         }, 0);
    //     } else if (tabs.length > 0) {
    //         // Default to first tab if no valid hash
    //         const defaultTab = tabs[0].getAttribute('data-tab');
    //         activateTab(defaultTab);
    //     }
    // }
    
    // // Handle tab clicks
    // tabs.forEach(tab => {
    //     tab.addEventListener('click', function(e) {
    //         const tabId = this.getAttribute('data-tab');
    //         // Update hash without causing scroll
    //         history.pushState(null, null, '#' + tabId);
    //         activateTab(tabId);
    //         // Prevent default behavior
    //         e.preventDefault();
    //     });
    // });
    
    // // Update dropdown links with custom click handlers
    // const accountLink = document.querySelector('a[href="{% url \'account\' %}"]');
    // if (accountLink) {
    //     accountLink.setAttribute('href', '{% url "account" %}#profile');
    //     accountLink.addEventListener('click', function(e) {
    //         e.preventDefault();
    //         history.pushState(null, null, '{% url "account" %}#profile');
    //         activateTab('profile');
    //     });
    // }
    
    // const ordersLink = document.querySelector('.orders-link');
    // if (ordersLink) {
    //     ordersLink.setAttribute('href', '{% url "account" %}#orders');
    //     ordersLink.addEventListener('click', function(e) {
    //         e.preventDefault();
    //         history.pushState(null, null, '{% url "account" %}#orders');
    //         activateTab('orders');
    //     });
    // }
    
    // // Listen for hash changes
    // window.addEventListener('hashchange', function(e) {
    //     // Prevent default scrolling behavior
    //     e.preventDefault();
    //     checkHash();
    // });
    
    // // Check hash on initial load
    // checkHash();


    const tabs = document.querySelectorAll('.account-nav li');
    const contentSections = document.querySelectorAll('.account-tab');
    
    // Function to activate tab based on ID without scrolling
    function activateTab(tabId) {
        // Remove active class from all tabs and content sections
        tabs.forEach(t => t.classList.remove('active'));
        contentSections.forEach(section => section.classList.remove('active'));
        
        // Add active class to current tab and content section
        const currentTab = document.querySelector(`.account-nav li[data-tab="${tabId}"]`);
        if (currentTab) {
            currentTab.classList.add('active');
            const contentSection = document.getElementById(tabId);
            if (contentSection) {
                contentSection.classList.add('active');
            }
        }
    }
    
    // Check URL hash on page load without scrolling
    function checkHash() {
        let hash = window.location.hash.substring(1); // Remove the # symbol
        if (hash && document.getElementById(hash)) {
            activateTab(hash);
            // Prevent scrolling to element
            setTimeout(function() {
                window.scrollTo(0, 0);
            }, 0);
        } else if (tabs.length > 0) {
            // Default to first tab if no valid hash
            const defaultTab = tabs[0].getAttribute('data-tab');
            activateTab(defaultTab);
        }
    }
    
    // Handle tab clicks
    tabs.forEach(tab => {
        tab.addEventListener('click', function(e) {
            const tabId = this.getAttribute('data-tab');
            // Update hash without causing scroll
            history.pushState(null, null, '#' + tabId);
            activateTab(tabId);
            // Prevent default behavior
            e.preventDefault();
        });
    });
    
    // Prevent dropdown links from having URL encoding issues
    const profileLink = document.querySelector('.profile-link');
    if (profileLink) {
        profileLink.addEventListener('click', function(e) {
            e.preventDefault();
            // Extract the base URL without template tags
            const baseUrl = window.location.pathname.split('#')[0];
            // Always set the complete absolute URL
            window.location.href = baseUrl + '#profile';
        });
    }
    
    const ordersLink = document.querySelector('.orders-link');
    if (ordersLink) {
        ordersLink.addEventListener('click', function(e) {
            e.preventDefault();
            // Extract the base URL without template tags
            const baseUrl = window.location.pathname.split('#')[0];
            // Always set the complete absolute URL
            window.location.href = baseUrl + '#orders';
        });
    }
    
    // Listen for hash changes
    window.addEventListener('hashchange', function(e) {
        // Prevent default scrolling behavior
        e.preventDefault();
        checkHash();
    });
    
    // Check hash on initial load
    checkHash();
    
    // Form validation for profile form
    const profileForm = document.querySelector('.profile-form');
    if (profileForm) {
        profileForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            const fullname = document.getElementById('fullname');
            const email = document.getElementById('email');
            const phone = document.getElementById('phone');
            const address = document.getElementById('address');
            
            let isValid = true;
            
            // Simple validation
            if (!fullname.value.trim()) {
                showError(fullname, 'Họ và tên không được để trống');
                isValid = false;
            } else {
                removeError(fullname);
            }
            
            if (!email.value.trim()) {
                showError(email, 'Email không được để trống');
                isValid = false;
            } else if (!isValidEmail(email.value.trim())) {
                showError(email, 'Email không hợp lệ');
                isValid = false;
            } else {
                removeError(email);
            }
            
            if (!phone.value.trim()) {
                showError(phone, 'Số điện thoại không được để trống');
                isValid = false;
            } else if (!isValidPhone(phone.value.trim())) {
                showError(phone, 'Số điện thoại không hợp lệ');
                isValid = false;
            } else {
                removeError(phone);
            }
            
            if (!address.value.trim()) {
                showError(address, 'Địa chỉ không được để trống');
                isValid = false;
            } else {
                removeError(address);
            }
            if (isValid) {
                // Show success message
                //showSuccessMessage('Cập nhật thông tin cá nhân thành công!');
                //showErrorMessage('Cập nhật thông tin cá nhân không thành công!');

                 // Chuẩn bị dữ liệu
                const formData = {
                    fullname: fullname.value.trim(),
                    email: email.value.trim(),
                    phone: phone.value.trim(),
                    address: address.value.trim(),
                    
                };

                // Gửi AJAX request
                fetch('/update_personal_info/', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-Requested-With': 'XMLHttpRequest',
                        'X-CSRFToken': csrftoken,
                    },
                    body: JSON.stringify(formData)
                })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        showSuccessMessage('Cập nhật thông tin cá nhân thành công!');
                    } else {
                        showErrorMessage('Có lỗi xảy ra khi cập nhật');
                    }
                })
                .catch(error => {
                    console.error('Error:', error);
                    showErrorMessage('Có lỗi xảy ra khi kết nối đến server');
                });
            }
        });
    }
    
    // Form validation for password change form
    const passwordForm = document.querySelector('.settings-form');
    if (passwordForm) {
        passwordForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            const currentPassword = document.getElementById('current-password');
            const newPassword = document.getElementById('new-password');
            const confirmPassword = document.getElementById('confirm-password');
            
            let isValid = true;
            
            if (!currentPassword.value) {
                showError(currentPassword, 'Vui lòng nhập mật khẩu hiện tại');
                isValid = false;
            } else {
                removeError(currentPassword);
            }
            
            if (!newPassword.value) {
                showError(newPassword, 'Vui lòng nhập mật khẩu mới');
                isValid = false;
            } else if (newPassword.value.length < 6) {
                showError(newPassword, 'Mật khẩu phải có ít nhất 6 ký tự');
                isValid = false;
            } else {
                removeError(newPassword);
            }
            
            if (!confirmPassword.value) {
                showError(confirmPassword, 'Vui lòng xác nhận mật khẩu mới');
                isValid = false;
            } else if (confirmPassword.value !== newPassword.value) {
                showError(confirmPassword, 'Mật khẩu xác nhận không khớp');
                isValid = false;
            } else {
                removeError(confirmPassword);
            }
            
            if (isValid) {
                // Show success message
                //showSuccessMessage('Cập nhật mật khẩu thành công!');
                
                // Reset form
                // passwordForm.reset();
                // Chuẩn bị dữ liệu
                const formData = {
                    current_password: currentPassword.value.trim(),
                    new_password: newPassword.value.trim(),
                    // confirm_password: confirmPassword.value.trim(),
                };
                // Gửi AJAX request
                fetch('/update_password/', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-Requested-With': 'XMLHttpRequest',
                        'X-CSRFToken': csrftoken,
                    },
                    body: JSON.stringify(formData)
                })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        showSuccessMessage('Cập nhật mật khẩu thành công!');
                        passwordForm.reset();
                        
                        setTimeout(() => {
                            window.location.href = '/loginregister/';
                        }, 3470); // đợi thông báo biến mất (~3 giây + hiệu ứng 0.5s)
                    } else {
                        showErrorMessage(data.error);
                    }
                })
            }
        });
    }
    
    // Delete account confirmation
    const deleteAccountBtn = document.querySelector('.danger-zone .btn-danger');
    if (deleteAccountBtn) {
        deleteAccountBtn.addEventListener('click', function() {
            if (confirm('Bạn có chắc chắn muốn xóa tài khoản? Hành động này không thể hoàn tác.')) {
                alert('Tài khoản đã được gửi yêu cầu xóa. Chúng tôi sẽ gửi email xác nhận cho bạn.');
            }
        });
    }
    
    // Order detail modal functionality
    const orderDetailModal = document.getElementById('orderDetailModal');
    const modalCloseButtons = document.querySelectorAll('.modal-close, .modal-close-btn');
    const orderDetailButtons = document.querySelectorAll('.order-actions .btn-outline');

    orderDetailButtons.forEach(button => {
        button.addEventListener('click', function() {
            const orderId = this.getAttribute('data-order-id');

            // Fetch order details dynamically
            fetch(`/order_detail_api/${orderId}/`)
                .then(response => response.json())
                .then(data => {
                    document.getElementById('modalOrderId').textContent = `#ORD-${data.order_id}`;
                    document.getElementById('modalCustomerName').textContent = data.customer_name;
                    document.getElementById('modalAddress').textContent = data.address;
                    document.getElementById('modalOrderDate').textContent = data.order_date;

                    const productList = document.getElementById('modalProductList');
                    productList.innerHTML = '';
                    data.products.forEach(product => {
                        const li = document.createElement('li');
                        li.textContent = `${product.name} - ${product.quantity} x ${product.price}`;
                        productList.appendChild(li);
                    });

                    document.getElementById('modalProductTotal').textContent = `${parseFloat(data.product_total).toFixed(2)}$`;
                    document.getElementById('modalShippingFee').textContent = data.shipping_fee;
                    document.getElementById('modalTotal').textContent = `${parseFloat(data.total).toFixed(2)}$`;

                    // Show modal
                    orderDetailModal.style.display = 'flex';
                })
                .catch(error => {
                    console.error('Error fetching order details:', error);
                });
        });
    });

    // Close modal
    modalCloseButtons.forEach(button => {
        button.addEventListener('click', function() {
            orderDetailModal.style.display = 'none';
        });
    });

    // Close modal when clicking outside
    orderDetailModal.addEventListener('click', function(e) {
        if (e.target === orderDetailModal) {
            orderDetailModal.style.display = 'none';
        }
    });
    
    // Helper functions
    function showError(input, message) {
        const formGroup = input.parentElement;
        let errorElement = formGroup.querySelector('.error-message');
        
        if (!errorElement) {
            errorElement = document.createElement('span');
            errorElement.className = 'error-message';
            errorElement.style.color = 'var(--danger-color)';
            errorElement.style.fontSize = '12px';
            errorElement.style.marginTop = '5px';
            errorElement.style.display = 'block';
            formGroup.appendChild(errorElement);
        }
        
        input.style.borderColor = 'var(--danger-color)';
        errorElement.textContent = message;
    }
    
    function removeError(input) {
        const formGroup = input.parentElement;
        const errorElement = formGroup.querySelector('.error-message');
        
        input.style.borderColor = '';
        
        if (errorElement) {
            errorElement.remove();
        }
    }
    
    function isValidEmail(email) {
        const re = /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
        return re.test(email.toLowerCase());
    }
    
    function isValidPhone(phone) {
        // Simple phone validation for Vietnamese numbers
        return /^(0|\+84)\d{9,10}$/.test(phone);
    }
    
    function showSuccessMessage(message) {
        const successAlert = document.createElement('div');
        successAlert.className = 'success-message';
        successAlert.style.backgroundColor = 'var(--success-color)';
        successAlert.style.color = 'white';
        successAlert.style.padding = '10px 15px';
        successAlert.style.borderRadius = '4px';
        successAlert.style.position = 'fixed';
        successAlert.style.top = '180px';
        successAlert.style.right = '20px';
        successAlert.style.zIndex = '1000';
        successAlert.style.boxShadow = '0 2px 10px rgba(0, 0, 0, 0.1)';
        successAlert.textContent = message;
    
        document.body.appendChild(successAlert);
    
        // Thêm lớp "show" để kích hoạt hiệu ứng trượt
        setTimeout(() => {
            successAlert.classList.add('show');
        }, 10); // Đợi một chút để trình duyệt áp dụng lớp CSS
    
        // Xóa thông báo sau 3 giây
        setTimeout(() => {
            successAlert.classList.remove('show'); // Trượt ra ngoài màn hình
            successAlert.style.opacity = '0'; // Mờ dần
    
            setTimeout(() => {
                successAlert.remove(); // Xóa khỏi DOM
            }, 500); // Đợi hiệu ứng kết thúc
        }, 3000);
    }
    
    function showErrorMessage(message) {
        const errorAlert = document.createElement('div');
        errorAlert.className = 'success-message';
        errorAlert.style.backgroundColor = 'var(--danger-color)';
        errorAlert.style.color = 'white';
        errorAlert.style.padding = '10px 15px';
        errorAlert.style.borderRadius = '4px';
        errorAlert.style.position = 'fixed';
        errorAlert.style.top = '180px';
        errorAlert.style.right = '20px';
        errorAlert.style.zIndex = '1000';
        errorAlert.style.boxShadow = '0 2px 10px rgba(0, 0, 0, 0.1)';
        errorAlert.textContent = message;
    
        document.body.appendChild(errorAlert);
    
        // Thêm lớp "show" để kích hoạt hiệu ứng trượt
        setTimeout(() => {
            errorAlert.classList.add('show');
        }, 10);
    
        // Xóa thông báo sau 3 giây
        setTimeout(() => {
            errorAlert.classList.remove('show');
            errorAlert.style.opacity = '0';
    
            setTimeout(() => {
                errorAlert.remove();
            }, 500);
        }, 3000);
    }
});


// Hàm để xử lý việc đặt hàng lại
        function reorderOrder(orderId) {
            // Hiển thị thông báo xác nhận
            Swal.fire({
                title: 'Xác nhận',
                text: 'Bạn có muốn mua lại các sản phẩm này không?',
                icon: 'question',
                showCancelButton: true,
                confirmButtonText: 'Đồng ý',
                cancelButtonText: 'Hủy',
            }).then((result) => {
                if (result.isConfirmed) {
                    // Gửi yêu cầu AJAX tới endpoint reorder
                    fetch(`/reorder/${orderId}/`, {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                            'X-CSRFToken': csrftoken,
                        },
                        
                    })
                    .then(response => response.json())
                    .then(data => {
                        if (data.success) {
                            // Hiển thị thông báo thành công
                            Swal.fire({
                                title: 'Thành công!',
                                text: 'Các sản phẩm đã được thêm vào giỏ hàng.',
                                icon: 'success',
                                confirmButtonText: 'OK'
                            }).then(() => {
                                // Hỏi người dùng muốn ở lại hay đến trang thanh toán
                                Swal.fire({
                                    title: 'Tiếp tục',
                                    text: 'Bạn muốn ở lại trang này hay đến trang thanh toán?',
                                    icon: 'question',
                                    showCancelButton: true,
                                    confirmButtonText: 'Đến trang thanh toán',
                                    cancelButtonText: 'Ở lại trang này'
                                }).then((result) => {
                                    if (result.isConfirmed) {
                                        window.location.href = '/checkout/';
                                    } else {
                                        updateCartCount();
                                    }
                                });
                            });
                        } else {
                            // Hiển thị thông báo lỗi
                            Swal.fire({
                                title: 'Lỗi!',
                                text: data.message || 'Có lỗi xảy ra khi thêm sản phẩm.',
                                icon: 'error',
                                confirmButtonText: 'OK'
                            });
                        }
                    })
                    .catch(error => {
                        // Xử lý lỗi mạng hoặc khác
                        Swal.fire({
                            title: 'Lỗi!',
                            text: 'Đã có lỗi xảy ra: ' + error.message,
                            icon: 'error',
                            confirmButtonText: 'OK'
                        });
                    });
                }
            });
        }
 


