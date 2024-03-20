function toggleWeekDetails(weekId) {
    const weekHeader = document.getElementById(`week-header-${weekId}`);
    weekHeader.classList.toggle('active-header');
    const weekDetails = document.getElementById(`week-details-${weekId}`);
    weekDetails.classList.toggle('active');
    const arrowIcon = document.getElementById(`arrow-icon-${weekId}`);
    arrowIcon.classList.toggle('flipped');
}

function clickFirstVisibleWeekHeader() {
    var firstVisibleWeekHeader = $('.week-header').parent(':not([style*="display: none"])').find('.week-header').first();
    if (firstVisibleWeekHeader.length > 0) {
        firstVisibleWeekHeader.click();
    }
}

$(document).ready(function() {
    
    $('#all-filter').prop('checked', true);
    $('.uresoldal').hide();

    $('.filter-tabs input[type="radio"]').change(function() {
        var selectedStatus = $(this).val();
        $('.a_het').each(function() {
            var $week = $(this);
            var hasTasksToShow = false;
            $week.find('.hf-doboz').each(function() {
                var $hfDoboz = $(this);
                if (selectedStatus === '' || $hfDoboz.hasClass(selectedStatus)) {
                    hasTasksToShow = true;
                    $hfDoboz.show();
                } else {
                    $hfDoboz.hide();
                }
            });
            if (hasTasksToShow) {
                $week.show();
                $('.uresoldal').hide();
            } else {
                $week.hide();
                $('.uresoldal').show();
            }
        });

        $('.week-header').removeClass('active-header');
        $('.week-details').removeClass('active');
        $('.arrow-icon').removeClass('flipped');
        
        clickFirstVisibleWeekHeader();
    });

    // Initial click for the first visible week header
    clickFirstVisibleWeekHeader();
});
