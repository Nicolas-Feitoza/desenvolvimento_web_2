document.addEventListener('DOMContentLoaded', function () {
    setTimeout(function () {
        let alerts = document.querySelectorAll('.alert');
        alerts.forEach(alert => {
            alert.style.transition = 'opacity 0.5s ease-out'; // Adiciona a transição
            alert.style.opacity = 0; // Define a opacidade para zero
            setTimeout(function () {
                alert.remove(); // Remove o alerta após a transição
            }, 1000) // Tempo de transição em milissegundos
        });
    }, 5000); // Tempo antes de começar a desaparecer em milissegundos
});
