/*
    KEY COMPONENTS:
    "entry" = Will contain id of entry.
    "user" = Will contain id of user.
    "rating" = user feedback about entry

    PROCESS:
    1 - User clicks one of 3 radio feedback options
    2 - Ajax sent to verify form and post rating to system
    4 - response includes average rating and total number of ratings entry has
    5 - update HTML for display rating and user input

 */
//get the CSRF_TOKEN
var csrftoken = document.getElementsByName('csrfmiddlewaretoken')[0].value;

// set array of selectors we want to match heights for:
var selectors = ['.carousel-title', '.item-count', '.slider-img', '.peerRating'];


//on ready function set handlers for rating click
$(document).ready(function () {

    // initial alignment
    alignItems(selectors, false);
    // add listener if user changes size of window/viewport
    window.addEventListener('resize', function () {
        alignItems(selectors, false);
    });

    // listen for ratings input
    var from = document.getElementById('submit-rating-form');
    from.addEventListener('submit', function (e) {
        e.preventDefault();
    });


    // set handlers for rating click
    $('.difficultyLevel').click(function () {
        var data = {
            'entry': $(this).data('entry'),
            'reviewer': $(this).data('reviewer'),
            'rating': $(this).data('rating'),
        };
        // send data to api View
        postRating(data);

    });

});

// send rating to api view url
function postRating(data) {
    var url = '/ratings/send';

    fetch(url,
        {
            method: 'post',
            credentials: 'include',
            headers: {
                'Content-type': 'application/json',
                'X-CSRFToken': csrftoken,
                'X-Requested-With': 'XMLHttpRequest'

            },
            body: JSON.stringify({
                'rating': data.rating,
                'reviewer': data.reviewer,
                'entry_id': data.entry,
                'csrfmiddlewaretoken': csrftoken,
            })
        })
        .then(response => response.json())
        .then(data => {
            updateAggregatedRating(data);
        })
        .catch((error) => {

        });
}

// process ajax and update aggregated display of trophy level
function updateAggregatedRating(data) {
    // clean out the existing content and rebuild it
    var contentHolder = $('.aggregate_rating_' + data['entry_id']);
    contentHolder.empty();
    // want hundreths
    var value = Math.round(parseFloat(data['trophies']) * 100) / 100;
    var new_content = '<div class="trophies" style="--rating: ' + value;
    new_content += '" aria-label="Rating of this product is ' + value + ' out of 3."></div>';
    contentHolder.append(new_content);
}

/*
    Carousel
*/
$('#carousel').on('slide.bs.carousel', function (e) {
    /*
        CC 2.0 License Iatek LLC 2018 - Attribution required
    */
    var $e = $(e.relatedTarget);
    var idx = $e.index();
    var itemsPerSlide = 2;
    var totalItems = $('.carousel-item').length;

    if (idx >= totalItems - (itemsPerSlide - 1)) {
        var it = itemsPerSlide - (totalItems - idx);
        for (var i = 0; i < it; i++) {
            // append slides to end
            if (e.direction == "left") {
                $('.carousel-item').eq(i).appendTo('.carousel-inner');
            } else {
                $('.carousel-item').eq(0).appendTo('.carousel-inner');
            }
        }
    }
});

