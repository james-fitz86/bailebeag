console.log("password reset form JS loaded");

document.addEventListener('DOMContentLoaded', () => {

    const form = document.querySelector("#password_reset_form");
    if (!form) return;

    const emailGroup     = form.querySelector('#div_id_email');
  
    const email     = emailGroup?.querySelector('input');

    const emailRegex    = /^\S+@\S+\.\S+$/;

    //Submit Validation
    form.addEventListener('submit', (e) => {
        let ok = true;
        //Validation Rules
       
        ok = ok && validateRequired(email, 'Email is required.');
        ok = ok && validatePattern(email, emailRegex, 'Please enter a valid email address.');


        if (!ok) e.preventDefault();
    });

    // Live Validation
    email?.addEventListener('input', () => {
        clearError(email);
        if (!email.value.trim()) return showError(email, 'Email is required.');
        if (!emailRegex.test(email.value)) showError(email, 'Please enter a valid email address.');
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