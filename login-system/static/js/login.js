// Enhanced form validation and UI interactions
document.addEventListener('DOMContentLoaded', function() {
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function(event) {
            const username = form.querySelector('#username').value.trim();
            const password = form.querySelector('#password').value.trim();

            // Clear previous errors
            clearErrors(form);

            let isValid = true;

            if (!username) {
                showError(form.querySelector('#username'), 'Username is required');
                isValid = false;
            } else if (username.length < 3) {
                showError(form.querySelector('#username'), 'Username must be at least 3 characters');
                isValid = false;
            }

            if (!password) {
                showError(form.querySelector('#password'), 'Password is required');
                isValid = false;
            } else if (password.length < 6) {
                showError(form.querySelector('#password'), 'Password must be at least 6 characters');
                isValid = false;
            }

            if (!isValid) {
                event.preventDefault();
                // Animate the form to draw attention
                form.style.animation = 'shake 0.5s';
                setTimeout(() => form.style.animation = '', 500);
            }
        });
    });

    // Add input focus effects
    const inputs = document.querySelectorAll('.form-control-user');
    inputs.forEach(input => {
        input.addEventListener('focus', function() {
            this.parentElement.classList.add('focused');
        });
        input.addEventListener('blur', function() {
            this.parentElement.classList.remove('focused');
        });
    });
});

function showError(element, message) {
    const errorDiv = document.createElement('div');
    errorDiv.className = 'invalid-feedback d-block';
    errorDiv.textContent = message;
    element.classList.add('is-invalid');
    element.parentElement.appendChild(errorDiv);
}

function clearErrors(form) {
    form.querySelectorAll('.is-invalid').forEach(el => el.classList.remove('is-invalid'));
    form.querySelectorAll('.invalid-feedback').forEach(el => el.remove());
}

// Add shake animation CSS via JS for dynamic effect
const style = document.createElement('style');
style.textContent = `
@keyframes shake {
    0%, 100% { transform: translateX(0); }
    10%, 30%, 50%, 70%, 90% { transform: translateX(-10px); }
    20%, 40%, 60%, 80% { transform: translateX(10px); }
}
.focused .form-control-user {
    border-color: #bac8f3;
    box-shadow: 0 0 0 0.2rem rgba(78, 115, 223, 0.25);
}
`;
document.head.appendChild(style);