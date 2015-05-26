/**
 * Created by ullmanfa on 13.05.15.
 */


$(document).ready(function () {

    if ($('.login-content')[0]) {

        $('body').on('click', '.login-navigation > li', function () {
            var z = $(this).data('block');
            var t = $(this).closest('.lc-block');

            t.removeClass('toggled');

            setTimeout(function () {
                $(z).addClass('toggled');
            });

        })
    }
})