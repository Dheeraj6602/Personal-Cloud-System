function toggleSection(sectionId) {
    var sections = document.querySelectorAll('section');
    sections.forEach(function (section) {
        if (section.id === sectionId) {
            section.style.display = 'block';
        } else {
            section.style.display = 'none';
        }
    });
}

// Add this script in your template
document.addEventListener('DOMContentLoaded', function () {
    var alerts = document.querySelectorAll('.alert_register, .alert_login');
    //var alert2 = document.querySelectorAll('.alert_login');
    alerts.forEach(function (alert) {
        setTimeout(function () {
            alert.style.display = 'none';
        }, 5000);  // Set the duration (in milliseconds) you want the alert to be displayed
    });
});





