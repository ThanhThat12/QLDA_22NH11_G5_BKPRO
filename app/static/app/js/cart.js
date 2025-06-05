// updateBtns = document.getElementsByClassName('update-cart')

// for (i = 0; i < updateBtns.length; i++) {
//     updateBtns[i].addEventListener('click', function(){
//         productId = this.dataset.product
//         action = this.dataset.action
//         console.log('productId:', productId, 'Action:', action)

//         console.log('USER:', user)
//         if (user === 'AnonymousUser'){
//             // Hiển thị popup khi chưa đăng nhập
//             Swal.fire({
//                 icon: 'warning',
//                 title: 'Bạn chưa đăng nhập',
//                 text: 'Vui lòng đăng nhập để thêm sản phẩm vào giỏ hàng.',
//                 confirmButtonText: 'Đăng nhập',
//                 showCancelButton: true,
//                 cancelButtonText: 'Hủy'
//             }).then((result) => {
//                 if (result.isConfirmed) {
//                     window.location.href = '/loginregister/'; // Chuyển hướng đến trang đăng nhập
//                 }
//             });
//         } else {
//             updateUserOrder(productId, action, this)
//         }
//     })
// }
document.addEventListener('click', function(event) {
    const button = event.target.closest('.update-cart');
    if (button) {
        const productId = button.dataset.product;
        const action = button.dataset.action;
        console.log('productId:', productId, 'Action:', action);

        console.log('USER:', user);
        if (user === 'AnonymousUser') {
            console.log('User is not authenticated');
            Swal.fire({
                icon: 'warning',
                title: 'Bạn chưa đăng nhập',
                text: 'Vui lòng đăng nhập để thêm sản phẩm vào giỏ hàng.',
                confirmButtonText: 'Đăng nhập',
                showCancelButton: true,
                cancelButtonText: 'Hủy'
            }).then((result) => {
                if (result.isConfirmed) {
                    window.location.href = '/loginregister/'; // Chuyển hướng đến trang đăng nhập
                }
            });
        } else {
            updateUserOrder(productId, action, button);
        }
    }
});

function updateUserOrder(productId, action, buttonElement) {
    if (action === 'add') {
        Swal.fire({
            title: 'Success!',
            text: 'Product has been added to the cart.',
            icon: 'success',
            confirmButtonText: 'OK'
        }).then(() => {
            fetch('/update_item/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrftoken,
                },
                body: JSON.stringify({ 'productId': productId, 'action': action })
            })
            .then(response => response.json())
            .then(data => {
                if (data.error) {
                    // Hiển thị popup nếu server trả về lỗi (ví dụ: phiên đăng nhập hết hạn)
                    Swal.fire({
                        icon: 'warning',
                        title: 'Lỗi',
                        text: data.error,
                        confirmButtonText: 'Đăng nhập',
                    }).then((result) => {
                        if (result.isConfirmed) {
                            window.location.href = '/loginregister/';
                        }
                    });
                } else {
                    updateCartCount();
                    updateCartTotal();
                }
            })
            .catch(error => console.error('Error updating cart:', error));
        });
    } else if (action === 'remove') {
        fetch('/update_item/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrftoken,
            },
            body: JSON.stringify({ 'productId': productId, 'action': 'check_quantity' }) // Check trước khi xóa
        })
        .then(response => response.json())
        .then(data => {
            console.log("Quantity received:", data.quantity);
            if (data.quantity === 1) {
                handleDeleteProduct(productId, 'delete', buttonElement);
            } else {
                fetch('/update_item/', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': csrftoken,
                    },
                    body: JSON.stringify({ 'productId': productId, 'action': action })
                })
                .then(response => response.json())
                .then(data => {
                    if (data.error) {
                        Swal.fire({
                            icon: 'warning',
                            title: 'Lỗi',
                            text: data.error,
                            confirmButtonText: 'Đăng nhập',
                        }).then((result) => {
                            if (result.isConfirmed) {
                                window.location.href = '/loginregister/';
                            }
                        });
                    } else {
                        updateCartCount();
                        updateCartTotal();
                    }
                })
                .catch(error => console.error('Error updating cart:', error));
            }
        })
        .catch(error => console.error('Error checking quantity:', error));
    } else if (action === 'add_cart') {
        fetch('/update_item/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrftoken,
            },
            body: JSON.stringify({ 'productId': productId, 'action': action })
        })
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                Swal.fire({
                    icon: 'warning',
                    title: 'Lỗi',
                    text: data.error,
                    confirmButtonText: 'Đăng nhập',
                }).then((result) => {
                    if (result.isConfirmed) {
                        window.location.href = '/loginregister/';
                    }
                });
            } else {
                updateCartCount();
                updateCartTotal();
            }
        })
        .catch(error => console.error('Error updating cart:', error));
    }
}

function updateCartCount() {
    fetch('/get_cart_count/')
    .then(response => response.json())
    .then(data => {
        document.getElementById('cart-count').textContent = data.cartItems;
        document.getElementById('total-items').textContent = data.cartItems;
        console.log('Cart count updated:', data.cartItems);
    })
    .catch(error => console.error('Error updating cart count:', error));
}

function updateCartTotal() {
    fetch('/get_cart_total/')
    .then(response => response.json())
    .then(data => {
        document.getElementById('cart-total').textContent = data.total_price + '$';
    })
    .catch(error => console.error('Error updating cart total:', error));
}

document.querySelectorAll('.delete-cart').forEach(button => {
    button.addEventListener('click', function() {
        const productId = this.dataset.product;
        const action = this.dataset.action;
        handleDeleteProduct(productId, action, this);
    });
});

function handleDeleteProduct(productId, action, buttonElement) {
    let productRow = buttonElement.closest('.cart-item');
    const quantityInput = productRow.querySelector('.txt-item-quantity');

    Swal.fire({
        title: 'Are you sure?',
        text: 'Do you want to delete this product from the cart?',
        icon: 'warning',
        showCancelButton: true,
        confirmButtonText: 'Yes, delete it!',
        cancelButtonText: 'No, keep it'
    }).then((result) => {
        if (result.isConfirmed) {
            fetch('/update_item/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrftoken,
                },
                body: JSON.stringify({ 'productId': productId, 'action': action })
            })
            .then(response => response.json())
            .then(data => {
                if (data.error) {
                    Swal.fire({
                        icon: 'warning',
                        title: 'Lỗi',
                        text: data.error,
                        confirmButtonText: 'Đăng nhập',
                    }).then((result) => {
                        if (result.isConfirmed) {
                            window.location.href = '/loginregister/';
                        }
                    });
                } else {
                    Swal.fire({
                        title: 'Deleted!',
                        text: 'Product has been deleted from the cart.',
                        icon: 'success',
                        confirmButtonText: 'OK'
                    }).then(() => {
                        if (productRow) {
                            productRow.remove();
                        }
                        updateCartCount();
                        updateCartTotal();
                    });
                }
            })
            .catch(error => console.error('Error deleting product:', error));
        } else {
            fetch('/get_item_quantity/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrftoken,
                },
                body: JSON.stringify({ 'productId': productId })
            })
            .then(response => response.json())
            .then(data => {
                if (quantityInput && data.quantity !== undefined) {
                    quantityInput.value = data.quantity;
                }
            })
            .catch(error => {
                console.error('Error fetching item quantity:', error);
            });
        }
    });
}