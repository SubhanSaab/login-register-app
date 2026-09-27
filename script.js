document.addEventListener('DOMContentLoaded', function () {
    const passwordInput = document.getElementById('password');

    if (passwordInput) {
        passwordInput.addEventListener('input', function () {
            if (passwordInput.value.length > 0 && passwordInput.value.length < 6) {
                passwordInput.setCustomValidity('Password must be at least 6 characters.');
            } else {
                passwordInput.setCustomValidity('');
            }
        });
    }
});