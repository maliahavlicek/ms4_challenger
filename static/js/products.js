/* JS for products page */

//on ready function
$(document).ready(function () {
    // initial alignment
    alignProducts();
    // add listener if user changes size of window/viewport
    window.addEventListener('resize', function () {
        alignProducts();
    });
});

function alignProducts() {
// figure out width of screen
    const vw = Math.max(document.documentElement.clientWidth || 0, window.innerWidth || 0);

    // set array of selectors we want to match heights for:
    var selectors = ['.card-header','.product-img-wrap', '.product-description', '.product-features', '.card-text.limits', '.card-text.price', '.card-footer'];
    $.each(selectors, function (index, selector) {
        // First auto height things
        var maxHeight = 'auto';
        $(selector).height(maxHeight);
        // next if larger than small devices, find max-height
        if (vw > 767) {
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


