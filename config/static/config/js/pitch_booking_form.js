console.log("pitch booking form JS loaded");

document.addEventListener('DOMContentLoaded', () => {

    

    const form = document.querySelector("#booking_form");
    if (!form) return;

    const nameGroup  = form.querySelector('#div_id_name');
    const emailGroup = form.querySelector('#div_id_email');
    const phoneGroup = form.querySelector('#div_id_phone');
    const startGroup = form.querySelector('#div_id_start_time');
    const endGroup = form.querySelector('#div_id_end_time');
    
    const pitch = form.querySelector('#id_pitch');
    const name  = nameGroup?.querySelector('input');
    const email = emailGroup?.querySelector('input');
    const phone = phoneGroup?.querySelector('input');
    const startInput  = startGroup?.querySelector('#id_start_time');
    const endInput    = endGroup?.querySelector('#id_end_time');

    const emailRegex    = /^\S+@\S+\.\S+$/;
    const phoneRegex  = /^[\d\s()+-]{7,}$/; 



    //Submit Validation
    form.addEventListener('submit', (e) => {
        let ok = true;
        //Validation Rules
        ok = ok && validateRequired(pitch, 'Please select a pitch.');

        ok = ok && validateRequired(name, 'Name is required.');
        ok = ok && validateMaxLength(name, 150, 'Name must be 150 characters or fewer');

        ok = ok && validateRequired(email, 'Email is required.');
        ok = ok && validatePattern(email, emailRegex, 'Please enter a valid email address.');

        ok = ok && validateRequired(phone, 'Phone number is required.');
        ok = ok && validatePattern(phone, phoneRegex, 'Please enter a valid email address.');

        ok = ok && validateRequired(startInput, 'Start time is required.');
        ok = ok && validateRequired(endInput, 'End time is required.');

        if (!ok) e.preventDefault();
    });

    // Live Validation
    pitch?.addEventListener('change', () => {
        clearError(pitch);
        if (!pitch.value.trim()) {
            showError(pitch, 'Please select a pitch.');
        }
    });

    name?.addEventListener('input', () => {
        clearError(name);
        if (!name.value.trim()) return showError(name, 'Name is required.');
        if (!nameRegex.test(name.value)) showError(name, 'Name must be 150 characters or fewer.');
    });

    email?.addEventListener('input', () => {
        clearError(email);
        if (!email.value.trim()) return showError(email, 'Email is required.');
        if (!emailRegex.test(email.value)) showError(email, 'Please enter a valid email address.');
    });

    phone?.addEventListener('input', () => {
      clearError(phone);
      if (!phone.value.trim()) return showError(phone, 'Phone is required.');
      if (!phoneRegex.test(phone.value)) showError(phone, 'Please enter a valid phone number.');
    });

    startInput?.addEventListener('change', () => {
        startInput.value = roundMinutes(startInput.value);
        endInput.value = addHour(startInput.value);
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
    // Helper function to remove the minutes from the user input so booking is always at the start of the hour
    function roundMinutes(input) {
        const userDate = new Date(input);
        
        const formattedDate = `${userDate.getFullYear()}-${String(userDate.getMonth()+1).padStart(2, '0')}-${String(userDate.getDate()).padStart(2, '0')}T${String(userDate.getHours()).padStart(2, '0')}:00`;
        
        return formattedDate;
        
    }

    // Helper function to set the end time as start time plus one hour, as bookings are limited to one hour slots
    function addHour(input) {
        const userDate = new Date(input);
        userDate.setHours(userDate.getHours()+1);

        const formattedEndDate = `${userDate.getFullYear()}-${String(userDate.getMonth()+1).padStart(2, '0')}-${String(userDate.getDate()).padStart(2, '0')}T${String(userDate.getHours()).padStart(2, '0')}:00`;

        return formattedEndDate;
    }
});
