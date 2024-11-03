// Password visibility on toggle for login/registration forms
function togglePasswordVisibility(passwordFieldId, toggleIconId) {
    const passwordField = document.querySelector(passwordFieldId);
    const toggleIcon = document.querySelector(toggleIconId);

    if (passwordField.type === 'password') {
        passwordField.type = 'text';
        toggleIcon.classList.remove('bi-eye');
        toggleIcon.classList.add('bi-eye-slash');
    } else {
        passwordField.type = 'password';
        toggleIcon.classList.remove('bi-eye-slash');
        toggleIcon.classList.add('bi-eye');
    }
}

document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('.input-group .form-control').forEach(input => {
        input.addEventListener('focus', () => {
            input.closest('.input-group').classList.add('focused');
        });

        input.addEventListener('blur', () => {
            input.closest('.input-group').classList.remove('focused');
        });
    });

    document.querySelectorAll('[data-toggle="password"]').forEach(button => {
        button.addEventListener('click', () => {
            const targetId = button.getAttribute('data-target');
            const iconId = button.getAttribute('data-icon');
            togglePasswordVisibility(targetId, iconId);
        });
    });
});