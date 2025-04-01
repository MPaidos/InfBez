const requiredInputs = document.querySelectorAll('input[required]');
const submitButton = document.getElementById('submitButton');
submitButton.disabled = true;
function validateForm() {
    var allFilled = true;
    requiredInputs.forEach(function(requiredInput) {
        if (requiredInput.value.trim() === '') {
            allFilled = false;
        }
    });
    submitButton.disabled = !allFilled;
}
requiredInputs.forEach(function(requiredInput) {
    requiredInput.addEventListener('change', function() {
        validateForm();
    });
});