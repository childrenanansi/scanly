$(document).ready(function() {
    // Слайдер — переключение слайдов
    function initSlider() {
        const track = $('.accounts-slider .accounts-slider-track');
        const slides = track.find('.accounts-slider-slide');
        track.data('current', 0);
        track.data('total', slides.length);
    }

    function updateNavButtons() {
        const track = $('.accounts-slider .accounts-slider-track');
        const current = parseInt(track.data('current'), 10) || 0;
        const total = parseInt(track.data('total'), 10) || 1;
        $('.popular-section:not(.popular-section-mockup) .prev-btn').prop('disabled', current === 0).toggleClass('disabled', current === 0);
        $('.popular-section:not(.popular-section-mockup) .next-btn').prop('disabled', current >= total - 1).toggleClass('disabled', current >= total - 1);
    }

    initSlider();
    updateNavButtons();

    $('.popular-section:not(.popular-section-mockup) .prev-btn').on('click', function() {
        const track = $(this).closest('.popular-section').find('.accounts-slider-track');
        let current = parseInt(track.data('current'), 10) || 0;
        const total = parseInt(track.data('total'), 10) || 1;
        if (current > 0) {
            current--;
            track.data('current', current);
            track.css('transform', `translateX(-${current * 100}%)`);
            updateNavButtons();
        }
    });

    $('.popular-section:not(.popular-section-mockup) .next-btn').on('click', function() {
        const track = $(this).closest('.popular-section').find('.accounts-slider-track');
        let current = parseInt(track.data('current'), 10) || 0;
        const total = parseInt(track.data('total'), 10) || 1;
        if (current < total - 1) {
            current++;
            track.data('current', current);
            track.css('transform', `translateX(-${current * 100}%)`);
            updateNavButtons();
        }
    });

    // Переключение вкладок навигации
    $('.nav-tabs-custom .nav-link').on('click', function(e) {
        e.preventDefault();
        $('.nav-tabs-custom .nav-link').removeClass('active');
        $(this).addClass('active');
    });
});
