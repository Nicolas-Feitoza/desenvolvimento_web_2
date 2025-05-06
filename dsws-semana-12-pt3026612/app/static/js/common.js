document.addEventListener('DOMContentLoaded', function () {
    // Remove automaticamente as mensagens flash após 5 segundos
    setTimeout(function () {
        let alerts = document.querySelectorAll('.alert');
        alerts.forEach(alert => alert.remove()); // Remove o elemento completamente
    }, 5000);

    // Evita submissão de formulário ao pressionar Enter
    document.querySelectorAll('form').forEach(function (form) {
        form.addEventListener('keypress', function (event) {
            if (event.key === 'Enter') {
                event.preventDefault();
                form.submit();
            }
        });
    });
});
