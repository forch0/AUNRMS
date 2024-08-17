document.addEventListener('DOMContentLoaded', function () {
    function updateSelectedCount() {
        const chosenPermissions = document.querySelectorAll('.selector .select2-selection__choice');
        const countDisplay = document.querySelector('.permission-count');
        if (countDisplay) {
            countDisplay.textContent = `${chosenPermissions.length} selected options`;
        }
    }

    // Update count on page load
    updateSelectedCount();

    // Update count whenever selection changes
    const selector = document.querySelector('.selector');
    if (selector) {
        $(selector).on('change.select2', function () {
            updateSelectedCount();
        });
    }
});
