document.addEventListener('DOMContentLoaded', function () {
    setTimeout(function () {
        let alerts = document.querySelectorAll('.alert');
        alerts.forEach(alert => {
            alert.remove(); // Remove o alerta
            alert.style.opacity = 0; // Opacidade zero após remoção
        });
    }, 5000);
});