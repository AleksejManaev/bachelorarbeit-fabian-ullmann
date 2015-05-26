/**
 * Created by ullmanfa on 13.05.15.
 */

(function ($) {
    $.fn.materialform = function () {
        var materialform = this;

        function SelectWrapper(select_wrapper) {
            var _this = this;
            _this.select_wrapper = select_wrapper;
            _this.addBtn = $(_this.select_wrapper).parent().find('a')[0];
            _this.list = $(_this.select_wrapper).find('select')[0];

            if (_this.addBtn) {
                $(_this.addBtn).addClass('fancybox').addClass('fancybox.iframe').fancybox({
                    type: 'ajax',
                    beforeShow: function () {
                        _this.form = $(' .fancybox-inner form');
                        _this.form.submit(function () {
                            selectWrapperSubmit(this, _this);
                        })
                    }
                })
            }

            _this.success = function (data) {
                $(_this.list).find('option[selected=selected]').removeAttr('selected');
                $(_this.list).append($(_this.list)
                    .find('option')
                    .last()
                    .clone()
                    .attr('selected', 'selected')
                    .attr('value', data[0].pk)
                    .text(data[0].fields.name));
                $(_this.list).material_select();
                $.fancybox.close();
            }

            _this.error = function (data) {
                _this.form.replaceWith($(data.responseText).find('form').submit(function () {
                    selectWrapperSubmit(this, _this);
                }));
            }

        };

        function selectWrapperSubmit(form, selectwrapper) {
            event.preventDefault();
            var form = $(form),
                selectwrapper = selectwrapper,
                formUrl = form.attr('action'),
                postData = new FormData(),
                data = form.serializeArray();

            $.each(data, function (key, input) {
                postData.append(input.name, input.value);
            });

            $.ajax({
                url: formUrl,
                data: postData,
                cache: false,
                contentType: false,
                processData: false,
                type: 'POST',
                success: function (data, status, jqXHR) {
                    selectwrapper.success(data)
                },
                error: function (data) {
                    selectwrapper.error(data);
                }
            })
        };

        $.each($(this).find('.select-wrapper'), function () {
            new SelectWrapper(this);
        });
    };
})(jQuery);


$(document).ready(
    function () {

        if ($('.card-reveal')[0]) {
            $('.card-reveal').show();
            $.each($('.card-reveal .card-content'), function (a, b) {
                $(b).css('min-height', $(b).parent().outerHeight() - $(b).parent().find('.card-header').outerHeight() - $(b).parent().find('.card-action').outerHeight());
            })
            $('.card-reveal').hide();
        }

        if ($('select')[0]) {
            $('select').material_select();
        }

        if ($('.datepicker')[0]) {
            $('.datepicker').removeClass('validate');
            $('.datepicker').pickadate({
                selectMonths: true, // Creates a dropdown to control month
                selectYears: 15, // Creates a dropdown of 15 years to control year
                format: 'yyyy-mm-dd'
            });

            $('.datepicker').on('change', function () {
                if ($(this).val()) {
                    $(this).removeClass('validate');
                    $(this).removeClass('invalid');
                    $(this).addClass('valid');

                } else {

                    $(this).removeClass('valid');
                    $(this).addClass('invalid');
                }
            })
        }

        $("form").materialform()

    }
)