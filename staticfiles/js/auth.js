// Password visibility on toggle for login forms

document.addEventListener('DOMContentLoaded', function () {
    const passwordToggle = document.getElementById('showPassword');
    const passwordField = document.getElementById('id_password');

    if (passwordToggle && passwordField) {
        passwordToggle.addEventListener('change', function () {
            passwordField.type = this.checked ? 'text' : 'password';
        });
    }
});