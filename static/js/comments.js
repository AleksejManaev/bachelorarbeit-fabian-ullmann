$(document).ready(function () {
    $(".btn-privacy").click(function () {
        var id = this.id;
        var btn = this;

        $.ajax({
            type: "POST",
            url: 'toggleprivacy',
            data: {csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(), id: id},
            datatype: "JSON",
            success: function (data) {
                var private_state = data['private_state'];
                var private_text = data['private_text'];

                if (private_state == true) {
                    $(btn).toggleClass('btn-warning btn-danger');
                    $(btn).html('<b>' + private_text + '</b>');
                }
                else if (private_state == false) {
                    $(btn).toggleClass('btn-danger btn-warning');
                    $(btn).html('<b>' + private_text + '</b>');
                }
            },
            failure: function (data) {
            }
        });
    });
});