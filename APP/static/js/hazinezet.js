function toggleWeekDetails(weekId) {
    const weekHeader = document.getElementById(`week-header-${weekId}`);
    weekHeader.classList.toggle('active-header');
    const weekDetails = document.getElementById(`week-details-${weekId}`);
    weekDetails.classList.toggle('active');
    const arrowIcon = document.getElementById(`arrow-icon-${weekId}`);
    arrowIcon.classList.toggle('flipped');
}

document.addEventListener("DOMContentLoaded", function() {
    // Wait for the DOM content to be fully loaded
    var firstWeekHeader = document.querySelector('.week-header');
    if (firstWeekHeader) {
        firstWeekHeader.click(); // Trigger click event on the first .week-header element
    }
});
