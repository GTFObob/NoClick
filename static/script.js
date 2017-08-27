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
        $.get('/summarize', req, function(res) {
            res = JSON.parse(res)
            update_display(res);

        }).fail(function(res) {
            console.log(res);
            var message;
            switch (res.status) {
                case 403:
                case 400:
                    message = "Please enter a valid URL and try again.";
                    break;
                default:
                    message = "An unknown error occurred."
            }

            $(".content .message").html(message);
            $('.page.dimmer:first')
                .dimmer('toggle');
        })

    })
});