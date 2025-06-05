document.addEventListener("DOMContentLoaded", () => {
    const container = document.getElementById("container");
    const registerBtn = document.getElementById("register");
    const loginBtn = document.getElementById("login");

    // Reset lỗi mặc định của input
    ["login-username", "login-password"].forEach(id => {
        const input = document.getElementById(id);
        if (input) input.setCustomValidity("");
    });

    // Bắt sự kiện chuyển tab
    registerBtn?.addEventListener("click", () => container.classList.add("right-panel-active"));
    loginBtn?.addEventListener("click", () => container.classList.remove("right-panel-active"));

    // Lấy dữ liệu từ server
    const isRegisterError = container.dataset.registerFailed === "true";
    const isRegisterSuccess = container.dataset.isRegisterSuccess === "true";
    const loginError = container.dataset.loginError;
    const isLoginSubmit = container.dataset.isLogin === "true";
    const isNotReload = container.dataset.isReload !== "true";
    const isRegisterQuery = new URLSearchParams(window.location.search).get("register") === "true";

    // Hiển thị thông báo đăng ký thành công (không chuyển tab)
    if (isRegisterSuccess && !isRegisterError && !isRegisterQuery) {
        const messages = document.querySelectorAll(".messages .alert");
        if (messages.length > 0) {
            Swal.fire({
                icon: "success",
                title: "Thành công",
                text: "Bạn đã đăng ký thành công! Vui lòng đăng nhập.",
                confirmButtonText: "OK",
                width: "400px", // Thu nhỏ popup
                padding: "1em",
                customClass: {
                    popup: "small-swal-popup",
                    title: "swal-title",
                    content: "swal-content",
                    confirmButton: "swal-confirm-button"
                },
                allowOutsideClick: false, // Ngăn người dùng click ngoài popup
                allowEscapeKey: false, // Ngăn đóng bằng phím Escape
                showCloseButton: false // Ẩn nút đóng
            });
        }
    }

    // Xử lý lỗi đăng ký
    if (isRegisterQuery || isRegisterError) {
        container.classList.add("right-panel-active");
        const errors = document.querySelectorAll(".register-container .error");
        errors.forEach(error => {
            const input = error.previousElementSibling;
            if (input && input instanceof HTMLInputElement) {
                input.setCustomValidity(error.textContent.trim());
                input.reportValidity();
                input.addEventListener("input", () => input.setCustomValidity(""));
            }
        });
    }

    // Xử lý lỗi đăng nhập
    if (isLoginSubmit && loginError && isNotReload) {
        container.classList.remove("right-panel-active");
        const usernameInput = document.getElementById("login-username");
        const passwordInput = document.getElementById("login-password");
        const isUsernameError = loginError.includes("Tài khoản") || loginError.includes("đầy đủ");
        const isPasswordError = loginError.includes("Mật khẩu");

        const target = isUsernameError ? usernameInput : passwordInput;
        target.setCustomValidity(loginError);
        target.reportValidity();
        target.addEventListener("input", () => target.setCustomValidity(""));
    }
});