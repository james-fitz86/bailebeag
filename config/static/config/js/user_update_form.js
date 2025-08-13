console.log("user update form JS loaded");

document.addEventListener('DOMContentLoaded', () => {

    const form = document.querySelector("#user_update_form");
    if (!form) return;

    const usernameGroup  = form.querySelector('#div_id_username');
    const firstNameGroup = form.querySelector('#div_id_first_name');
    const lastNameGroup = form.querySelector('#div_id_last_name');
    const emailGroup     = form.querySelector('#div_id_email');
  
    const username  = usernameGroup?.querySelector('input');
    const firstName = firstNameGroup?.querySelector('input');
    const lastName = lastNameGroup?.querySelector('input');
    const email     = emailGroup?.querySelector('input');
    

    const usernameRegex = /^[\w.@+-]{1,150}$/;
    const emailRegex    = /^\S+@\S+\.\S+$/;

    //Submit Validation
    form.addEventListener('submit', (e) => {
        let ok = true;
        //Validation Rules
        ok = ok && validateRequired(username, 'Username is required.');
        ok = ok && validatePattern(username, usernameRegex, 'Username must be 150 characters or fewer. Letters, digits and @/./+/-/_ only.');

        ok = ok && validateRequired(email, 'Email is required.');
        ok = ok && validatePattern(email, emailRegex, 'Please enter a valid email address.');

        ok = ok && validateRequired(firstName, 'First Name is required.');
        ok = ok && validateMaxLength(firstName, 150, 'First Name must be 150 characters or fewer');

        ok = ok && validateRequired(lastName, 'Last Name is required.');
        ok = ok && validateMaxLength(lastName, 150, 'Last Name must be 150 characters or fewer');

        if (!ok) e.preventDefault();
    });

    // Live Validation
    username?.addEventListener('input', () => {
        clearError(username);
        if (!username.value.trim()) return showError(username, 'Username is required.');
        if (!usernameRegex.test(username.value)) showError(username, 'Username must be 150 characters or fewer. Letters, digits and @/./+/-/_ only.');
    });

    email?.addEventListener('input', () => {
        clearError(email);
        if (!email.value.trim()) return showError(email, 'Email is required.');
        if (!emailRegex.test(email.value)) showError(email, 'Please enter a valid email address.');
    });

    firstName?.addEventListener('input', () => {
        clearError(firstName);
        if (!firstName.value.trim()) return showError(firstName, 'First Name is required.');;
        if (!firstNameRegex.test(firstName.value)) showError(firstName, 'First Name must be 150 characters or fewer');
    });

    lastName?.addEventListener('input', () => {
        clearError(lastName);
        if (!lastName.value.trim()) return showError(lastName, 'Last Name is required.');
        if (!lastNameRegex.test(lastName.value)) showError(lastName, 'Last Name must be 150 characters or fewer');
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

    function validateMaxLength(input, maxLength, message) {
        if (input.value.trim().length > maxLength) {
        showError(input, message);
        return false;
        }
        return true;
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