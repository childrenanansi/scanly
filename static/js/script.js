$(document).ready(function() {
    // Слайдер — карусель с бесконечным циклом
    function getCardsPerSlide() {
        const width = window.innerWidth;
        if (width >= 1200) return 6;      // Desktop
        if (width >= 992) return 4;       // Large tablets
        if (width >= 768) return 2;       // Tablets
        return 1;                         // Mobile
    }

    function initSlider() {
        const track = $('.accounts-slider .accounts-slider-track');
        const slides = track.find('.accounts-slider-slide');
        
        if (slides.length === 0) return;
        
        const cardsPerSlide = getCardsPerSlide();
        const totalSlides = Math.ceil(slides.length / cardsPerSlide);
        
        // Группируем слайды и дублируем группы
        const slideGroups = [];
        for (let i = 0; i < slides.length; i += cardsPerSlide) {
            const group = slides.slice(i, i + cardsPerSlide);
            slideGroups.push(group);
        }
        
        // Создаем HTML для групп
        const groupsHTML = slideGroups.map(group => {
            const groupHTML = $('<div>').append(group.clone()).html();
            return `<div class="accounts-slider-slide-group" style="display: flex; gap: 20px; padding: 0 15px;">${groupHTML}</div>`;
        }).join('');
        
        // Очищаем и добавляем группы
        track.empty();
        track.append(groupsHTML); // Оригинальные группы
        track.append(groupsHTML); // Дубликат в конец
        track.append(groupsHTML); // Дубликат в начало
        
        // Устанавливаем начальную позицию
        const totalOriginalGroups = slideGroups.length;
        track.data('current', totalOriginalGroups);
        track.data('totalOriginal', totalOriginalGroups);
        track.data('totalGroups', totalOriginalGroups * 3);
        
        updateSlider(false);
    }

    function updateSlider(animate = true) {
        const track = $('.accounts-slider .accounts-slider-track');
        const current = parseInt(track.data('current'), 10) || 0;
        
        if (!animate) {
            track.css('transition', 'none');
        } else {
            track.css('transition', 'transform 0.4s ease');
        }
        
        track.css('transform', `translateX(-${current * 100}%)`);
        
        // Проверяем необходимость бесконечного перехода
        setTimeout(function() {
            checkInfiniteLoop();
        }, animate ? 400 : 0);
    }

    function checkInfiniteLoop() {
        const track = $('.accounts-slider .accounts-slider-track');
        const current = parseInt(track.data('current'), 10) || 0;
        const totalOriginal = parseInt(track.data('totalOriginal'), 10) || 1;
        
        // Если дошли до конца
        if (current >= totalOriginal * 2) {
            track.data('current', totalOriginal);
            track.css('transition', 'none');
            track.css('transform', `translateX(-${totalOriginal * 100}%)`);
            setTimeout(() => {
                track.css('transition', 'transform 0.4s ease');
            }, 50);
        }
        
        // Если дошли до начала
        if (current < totalOriginal) {
            track.data('current', totalOriginal);
            track.css('transition', 'none');
            track.css('transform', `translateX(-${totalOriginal * 100}%)`);
            setTimeout(() => {
                track.css('transition', 'transform 0.4s ease');
            }, 50);
        }
    }

    function nextSlide() {
        const track = $('.accounts-slider .accounts-slider-track');
        let current = parseInt(track.data('current'), 10) || 0;
        current++;
        track.data('current', current);
        updateSlider(true);
    }

    function prevSlide() {
        const track = $('.accounts-slider .accounts-slider-track');
        let current = parseInt(track.data('current'), 10) || 0;
        current--;
        track.data('current', current);
        updateSlider(true);
    }

    // Initialize slider
    initSlider();

    $('.popular-section:not(.popular-section-mockup) .prev-btn').on('click', function(e) {
        e.preventDefault();
        prevSlide();
    });

    $('.popular-section:not(.popular-section-mockup) .next-btn').on('click', function(e) {
        e.preventDefault();
        nextSlide();
    });

    // Auto-play (опционально)
    let autoplayInterval;
    function startAutoplay() {
        autoplayInterval = setInterval(nextSlide, 4000); // 4 секунды
    }

    function stopAutoplay() {
        clearInterval(autoplayInterval);
    }

    // Запускаем автопроигрывание
    startAutoplay();

    // Останавливаем при наведении мыши
    $('.accounts-slider').on('mouseenter', stopAutoplay);
    $('.accounts-slider').on('mouseleave', startAutoplay);

    // Update slider on window resize
    let resizeTimer;
    $(window).on('resize', function() {
        clearTimeout(resizeTimer);
        resizeTimer = setTimeout(function() {
            stopAutoplay();
            initSlider();
            startAutoplay();
        }, 250);
    });

    // Touch/swipe support для мобильных
    let touchStartX = 0;
    let touchEndX = 0;
    
    $('.accounts-slider').on('touchstart', function(e) {
        touchStartX = e.originalEvent.touches[0].clientX;
    });
    
    $('.accounts-slider').on('touchend', function(e) {
        touchEndX = e.originalEvent.changedTouches[0].clientX;
        handleSwipe();
    });
    
    function handleSwipe() {
        const swipeThreshold = 50;
        const diff = touchStartX - touchEndX;
        
        if (Math.abs(diff) > swipeThreshold) {
            if (diff > 0) {
                nextSlide(); // Свайп влево - следующий слайд
            } else {
                prevSlide(); // Свайп вправо - предыдущий слайд
            }
        }
    }

});
