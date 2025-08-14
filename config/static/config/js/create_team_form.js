console.log("create team booking form JS loaded");

document.addEventListener('DOMContentLoaded', () => {

    const form = document.querySelector("#create_team_form");
    if (!form) return;

    const ageGroup = form.querySelector('#id_age_group');
    const gender = form.querySelector('#id_gender');
    const sport = form.querySelector('#id_sport');


    //Submit Validation
    form.addEventListener('submit', (e) => {
        let ok = true;
        //Validation Rules
        ok = ok && validateRequired(ageGroup, 'Please select an Age group.');
        ok = ok && validateRequired(gender, 'Please select a Gender.');
        ok = ok && validateRequired(sport, 'Please select a Sport.');

        if (!ok) e.preventDefault();
    });

    // Live Validation
    ageGroup?.addEventListener('change', () => {
        clearError(ageGroup);
        if (!ageGroup.value.trim()) {
            showError(ageGroup, 'Please select an Age group.');
        }
    });
    gender?.addEventListener('change', () => {
        clearError(gender);
        if (!gender.value.trim()) {
            showError(gender, 'Please select a Gender.');
        }
    });
    sport?.addEventListener('change', () => {
        clearError(sport);
        if (!sport.value.trim()) {
            showError(sport, 'Please select a Sport.');
        }
    });


    //Helpers
    function validateRequired(input, message) {
        if (!input || input.value.trim()) return true;
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