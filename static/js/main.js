document.addEventListener('DOMContentLoaded', function() {
    // Устанавливаем начальный цвет фона (по умолчанию белый)
    document.body.style.backgroundColor = 'lightblue';

    // Меняем цвет фона на голубой при клике на любую ссылку
    const navLinks = document.querySelectorAll('.nav-list li a');

    navLinks.forEach(link => {
        link.addEventListener('click', function() {
            // Изменяем фон на голубой
            document.body.style.backgroundColor = 'lightblue';
        });
    });
});