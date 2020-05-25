/* utils.js - holds utility functions used on more than one page */


/* Match heights of items on page based on incoming array of selectors */
function alignItems(selectors, skipSmall) {
    var skip_small = (typeof skipSmall === 'undefined') ? true : skip_small;

// figure out width of screen
    const vw = Math.max(document.documentElement.clientWidth || 0, window.innerWidth || 0);
    $.each(selectors, function (index, selector) {
        // First auto height things
        var maxHeight = 'auto';
        $(selector).height(maxHeight);
        // next if larger than small devices, or if skipSmall is false find max-height and even things up
        if (vw > 767 || !skip_small) {
            var maxHeight = 0;

            // loop through list of selectors to get maxHeight
            $(selector).each(function () {
                if ($(this).height() > maxHeight) {
                    maxHeight = $(this).height();
                }
            });

            // set all of that selector to the same height
            $(selector).height(maxHeight);

        }
    });
}