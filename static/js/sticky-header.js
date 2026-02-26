/**
 * Sticky Header functionality
 * Добавляет полупрозрачный фон для header при прокрутке
 */
$(document).ready(function() {
    const $header = $('#main-header');
    
    if ($header.length) {
        // Функция для проверки прокрутки и добавления класса
        function handleScroll() {
            if ($(window).scrollTop() > 50) { // Добавляем класс после прокрутки на 50px
                $header.addClass('sticky');
            } else {
                $header.removeClass('sticky');
            }
        }
        
        // Проверяем при загрузке страницы
        handleScroll();
        
        // Добавляем обработчик события прокрутки
        $(window).on('scroll', handleScroll);
    }
});
