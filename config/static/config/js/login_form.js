console.log("login form JS loaded");

document.addEventListener('DOMContentLoaded', () => {

    const form = document.querySelector("#login_form");
    if (!form) return;

    const usernameGroup  = form.querySelector('#div_id_username');
    const passwordGroup = form.querySelector('#div_id_password');
  
    const username  = usernameGroup?.querySelector('input');
    const password = passwordGroup?.querySelector('input');

    const usernameRegex = /^[\w.@+-]{1,150}$/;
    const passwordRegex = /^(?!^\d+$).{8,}$/;

    //Submit Validation
    form.addEventListener('submit', (e) => {
        let ok = true;
        //Validation Rules
        ok = ok && validateRequired(username, 'Username is required.');
        ok = ok && validatePattern(username, usernameRegex, 'Username must be 150 characters or fewer. Letters, digits and @/./+/-/_ only.');

        ok = ok && validateRequired(password, 'Password is required.');
        ok = ok && validatePattern(password, passwordRegex, 'Password must be at least 8 characters and cannot be entirely numeric.');

        if (!ok) e.preventDefault();
    });

    // Live Validation
    username?.addEventListener('input', () => {
        clearError(username);
        if (!username.value.trim()) return showError(username, 'Username is required.');
        if (!usernameRegex.test(username.value)) showError(username, 'Username must be 150 characters or fewer. Letters, digits and @/./+/-/_ only.');
    });

    password?.addEventListener('input', () => {
        clearError(password);
        const val = password.value;

        if (!val.trim()) return showError(password, 'Password is required.');
        if (val.length < 8) return showError(password, 'Password must be at least 8 characters.');
        if (/^\d+$/.test(val)) return showError(password, 'Password cannot be entirely numeric.');
    });

    //Helpers
    function validateRequired(input, message) {
        if (!input || input.value.trim()) return true;
        showError(input, message);
        return false;
        }

    function validatePattern(input, regex, message) {
        if (!input) return true;
        if (input.value && regex.test(input.value)) return true;
        showError(input, message);
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