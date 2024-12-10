window.addEventListener('resize', function() {
    if (window.innerWidth < 940) {
        var mobileBars = document.querySelectorAll('.mobile-bar.show');
        if (mobileBars.length > 0) {
            OpenMenu();
        }
    }
});