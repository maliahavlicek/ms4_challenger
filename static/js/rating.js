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


//on ready function set handlers for rating click
$(document).ready(function () {
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
            method: 'POST',
            headers: {
                'Content-type': 'application/json',
                'X-CSRFTOKEN': csrftoken,

            },
            body: JSON.stringify({
                    'rating': data.rating,
                    'reviewer': data.reviewer,
                    'entry_id': data.entry,
                })
        })
        .then(response => response.json())
        .then(data => {
            console.log('Success:', data);
            updateAggregatedRating(data);
        })
        .catch((error) => {
            console.error('Error:', error);
        });
}

// process ajax and update aggregated display of trophy level
function updateAggregatedRating(data){
    $('#aggregate_rating_txt_'+data['entry_id']).innerHTML= data['trophies'];
    var percent = Math.round(parseFloat(data['trophies'])/3* 100)/100;
    $('#aggregate_rating_pb_'+data['entry_id']).width(percent);

    //tyle="height:30px;width:{{ item.get_rating|percent_rating }}"
}
