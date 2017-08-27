API = 'http://0.0.0.0:5000/summarize'

function update_display(elements) {
    console.log(elements);

    $('#response h2').text(elements.title);

    $("#response li").remove();
    var res_ul = $("#response ul")

    $.each(elements.content, function(i, element) {
        res_ul.append('<li>' + element + '</li>')
    })

    $("#response").removeClass("disabled");
}

$(function() {
    $("#search-button").click(function() {
        req = { url: $("#search-input").val() }
        $.get(API, req, function(res) {
            res = JSON.parse(res)
            update_display(res);

        }).fail(function(res) {
            console.log(res);
            switch (res.status) {
                case 403:
                case 400:
                    $(".content .message").html("Please enter a valid URL and try again.");
                    break;
            }


            $('.page.dimmer:first')
                .dimmer('toggle');
        })

    })
});