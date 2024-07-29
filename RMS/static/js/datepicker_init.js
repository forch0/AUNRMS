// static/js/datepicker_init.js
document.addEventListener('DOMContentLoaded', function() {
    var datepickers = document.querySelectorAll('.datepicker');
    datepickers.forEach(function(datepicker) {
        $(datepicker).datepicker({
            format: 'yyyy-mm-dd',
            autoclose: true,
            todayHighlight: true
        });
    });
});
