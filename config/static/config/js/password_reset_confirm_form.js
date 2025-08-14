console.log("passowrd reset confirm form JS loaded");

document.addEventListener('DOMContentLoaded', () => {

    const form = document.querySelector("#password_reset_confirm_form");
    if (!form) return;

    const password1Group = form.querySelector('#div_id_new_password1');
    const password2Group = form.querySelector('#div_id_new_password2');
  
    const password1 = password1Group?.querySelector('input');
    const password2 = password2Group?.querySelector('input');

    const emailRegex    = /^\S+@\S+\.\S+$/;

    //Submit Validation
    form.addEventListener('submit', (e) => {
        let ok = true;
        //Validation Rules
        ok = ok && validateRequired(password1, 'Password is required.');
        ok = ok && validateRequired(password2, 'Confirm your password.');
        ok = ok && validatePasswordsMatch(password1, password2, 'Passwords do not match.');

        if (!ok) e.preventDefault();
    });
    
    //Password Synchronisation
    const syncPasswords = () => {
        clearError(password1);
        clearError(password2);
        if (!password1.value || !password2.value) return;
        if (password1.value !== password2.value) {
        showError(password2, 'Passwords do not match.');
        
        password2.setCustomValidity('Passwords do not match.');
        } else {
        password2.setCustomValidity('');
        }
    };
    password1?.addEventListener('input', syncPasswords);
    password2?.addEventListener('input', syncPasswords);

    //Helpers
    function validateRequired(input, message) {
        if (!input || input.value.trim()) return true;
        showError(input, message);
        return false;
        }

    function validatePasswordsMatch(pw1, pw2, message) {
        if (!pw1 || !pw2) return true;
        if (!pw1.value || !pw2.value) return true;
        if (pw1.value === pw2.value) return true;
        showError(pw2, message);
        return false;
    }

    function showError(input, message) {
        
        input.classList.add('is-invalid');

        
        let fb = input.parentElement.querySelector('.invalid-feedback');
        if (!fb) {
        fb = document.createElement('div');
        fb.className = 'invalid-feedback';
        
        input.insertAdjacentElement('afterend', fb);
        }
        fb.textContent = message;
    }

    function clearError(input) {
        input.classList.remove('is-invalid');
        const fb = input.parentElement.querySelector('.invalid-feedback');
        
        const next = input.nextElementSibling;
        if (next && next.classList.contains('invalid-feedback')) {
        next.remove();
        } else if (fb) {
        
        fb.remove();
        }
        
        if (typeof input.setCustomValidity === 'function') input.setCustomValidity('');
    }
});