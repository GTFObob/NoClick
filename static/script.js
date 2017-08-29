function update_display(elements) {
    console.log(elements);

    $('#response h2').text(elements.title);

    $("#response li").remove();
    var res_ul = $("#response ul")

    $.each(elements.content, function(i, element) {
        res_ul.append('<li>' + element + '</li>')
    })

    $("#response").removeClass("loading");
}

$(function() {
    $("#search-button").click(function() {
        req = { url: $("#search-input").val() }

        $.get({
            url: '/summarize',
            data: req,
            dataType: "json",
            beforeSend: function() {
                $("#response").removeClass("disabled");
                $("#response").addClass("loading");
            },
            success: function(res) {
                update_display(res);
            },
            error: function(res) {
                var message;
                switch (res.status) {
                    case 403:
                    case 400:
                        message = "Please enter a valid URL and try again.";
                        break;
                    default:
                        message = "An unknown error occurred."
                }

                $("#response").removeClass("loading");
                $("#response").addClass("disabled");

                $(".content .message").html(message);
                $('.page.dimmer:first')
                    .dimmer('toggle');

            }
        })
    })
});