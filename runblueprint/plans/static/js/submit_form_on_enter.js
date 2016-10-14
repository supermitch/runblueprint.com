$(document).ready(function() {
    $('enter-to-submit').keydown(function(event) {
        if (event.keyCode == 13) {
            this.form.submit();
            return false;
        }
    });
});
