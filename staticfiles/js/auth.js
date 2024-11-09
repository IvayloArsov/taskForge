// Password visibility on toggle for login/registration forms

document.addEventListener('DOMContentLoaded', function() {
    // Password visibility toggle
    document.querySelectorAll('[data-password-toggle]').forEach(button => {
        button.addEventListener('click', function() {
            const passwordId = this.getAttribute('data-password-toggle');
            const passwordField = document.getElementById(passwordId);
            const icon = this.querySelector('i');

            if (passwordField.type === 'password') {
                passwordField.type = 'text';
                icon.classList.remove('bi-eye');
                icon.classList.add('bi-eye-slash');
            } else {
                passwordField.type = 'password';
                icon.classList.remove('bi-eye-slash');
                icon.classList.add('bi-eye');
            }
        });
    });

    document.querySelectorAll('.input-group .form-control').forEach(input => {
        input.addEventListener('focus', () => {
            input.closest('.input-group').classList.add('focused');
        });

        input.addEventListener('blur', () => {
            input.closest('.input-group').classList.remove('focused');
        });
    });
});
