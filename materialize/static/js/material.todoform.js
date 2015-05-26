/**
 * Created by ullmanfa on 17.05.15.
 */
function setContentHeight(param, cr_content) {

    my_height = $(cr_content).outerHeight();
    parent_height = $(param).find('> .card-content').height();

    if (my_height > parent_height) {
        $(param).find('> .card-content').first().css({'height': $(cr_content).outerHeight()});
    } else {
        $(param).find('> .card-content').first().css({'height': $(cr_content).css('min-height')});
    }
}
(function ($) {
    $.fn.todoList = function () {

        $(document).off('click.card', '.card');
        var _this = this,
            form = $(this).parent(),
            reveal = {

                addContent: function (from) {
                    var _from = from || _this;

                    //var inp_target = $(_from).find('#' + $(this.target).attr('id').replace('_todo', '')).parents('.input-field.hide');

                    var inp_target = $(_from).find('#' + $(this.target).attr('id').replace('_todo', '')).parents('.input-field.hide');

                    if (!inp_target[0]) {
                        inp_target = $(this.target).parents('.todo-item').find('.input-group.hide')
                    }

                    $(this.title).text($(this.target).parent().find('label').text());
                    $(this.title).append(this.close_btn);
                    $(this.content).html(inp_target.removeClass('hide'));
                    $(this.reveal).show();
                    this.input = $(this.reveal).find('input, textarea, select');
                    this.input_original = this.input.clone();
                    this.state = '';

                    if (this.target.indeterminate) {
                        this.state = 'changed'
                    }
                    ;

                    // File Input Path
                    this.content.find('.file-field').each(function () {
                        var path_input = $(this).find('input.file-path');
                        $(this).find('input[type="file"]').change(function () {
                            path_input.val($(this)[0].files[0].name);
                            path_input.trigger('change');
                        });
                    });

                    this.contentAdded();

                },
                bindButtons: function () {
                    this.close_btn.parent().on('click', function (e) {
                        reveal.hide();
                    });

                    this.cancel_btn.on('click', function (e) {
                        e.preventDefault();
                        reveal.state = 'canceled';
                        reveal.cancel()
                    });

                    this.save_btn.on('click', function (e) {
                        e.preventDefault();
                        if (reveal.state == 'changed') {
                            reveal.save();
                        } else {
                            reveal.hide();
                        }
                    });
                },
                cancel: function () {
                    $.ajax({
                        url: form.attr('action'),
                        type: 'GET',
                        success: function (data) {
                            reveal.post_data = data;
                            reveal.state = 'canceled';
                            reveal.hide();
                        }
                    });
                },
                contentAdded: function () {
                    this.unbindButtons();
                    this.bindButtons();
                    $(this.input).bind('paste, keyup', function () {
                        setTimeout(function () {
                            setContentHeight(_this, reveal.content);
                        }, 300);
                    });
                    $(this.input).on('change', function () {
                        reveal.state = 'changed';
                        $(this).off('change');
                    });

                    setContentHeight(_this, this.content);
                },
                hide: function () {
                    $(this.reveal).velocity("stop", false).velocity(
                        {translateY: 0}, {
                            duration: 225,
                            queue: false,
                            easing: 'easeInOutQuad',
                            complete: reveal.hideComplete
                        }
                    );
                },
                hideComplete: function (e) {
                    reveal.unbindButtons();
                    reveal.removeContent();
                },
                init: function () {
                    this.reveal = $(_this).find('.card-reveal');
                    this.title = this.reveal.find('.card-title');
                    this.content = this.reveal.find('.card-content');
                    this.close_btn = this.reveal.find('.card-title i');
                    this.cancel_btn = this.reveal.find('.card-action a[data-cr-action=dismiss]');
                    this.save_btn = this.reveal.find('.card-action a[data-cr-action=save]');

                },
                removeContent: function () {
                    var current = $(this.content).find('.input-field, .input-group')[0],
                        target = $(_this).find('> .card-content .todo-item:not(:has(.input-field))').first();

                    switch (this.state) {
                        case 'changed':
                            target.find('.activator').prop("indeterminate", true);
                            break;
                        case 'saved':
                            target.find('.activator').prop("indeterminate", false);
                            if ((($(current).find('.valid')[0] && !$(current).find('.invalid')[0]) || $(this.content).find('.select-wrapper')[0])
                                && !$(this.content).find('input[id$="clear_id"]:checked')[0]
                                && !Boolean(Boolean($(this.content).find('option:selected')[0])
                                    && !Boolean($(this.content).find('option:selected').val()))) {
                                target.find('.activator').prop("checked", true);
                            } else {
                                target.find('.activator').prop("checked", false);
                            }
                            break;
                        case 'error':
                            target.find('.activator').prop("checked", false);
                            target.find('.activator').prop("indeterminate", true);
                            break;
                        case 'canceled':
                            target.find('.activator').prop("indeterminate", false);
                            break;
                        default :
                            break;
                    }

                    target.append($(current).addClass('hide'));
                    this.setPostData();

                    setContentHeight(_this, this.content);
                },
                save: function () {
                    var formUrl = form.attr('action'),
                        postData = new FormData(),
                        mainData = form.serializeArray(),
                        input = this.content.find('input[id], textarea[id]');
                    $.each(mainData, function (key, input) {
                        if (input.name == 'csrfmiddlewaretoken') {
                            postData.append(input.name, input.value);
                        } else {
                            postData.append(input.name, input.value);
                        }
                    });


                    $.each(input, function (i, file) {
                        if (input[i].files) {
                            $.each(input[i].files, function (i, file) {
                                postData.append($(input[i]).attr('name'), file);
                            })
                        } else {
                            postData.append(input.name, input.value);
                        }
                    });

                    $.ajax(
                        {
                            url: formUrl,
                            data: postData,
                            cache: false,
                            contentType: false,
                            processData: false,
                            type: 'POST',
                            success: function (data, textStatus, jqXHR) {
                                //data: return data from server
                                //Materialize.toast("saved", 2000, 'green');

                                reveal.post_data = data;
                                reveal.state = 'saved';
                                reveal.hide();
                            },
                            error: function (jqXHR, textStatus, errorThrown) {
                                Materialize.toast("Input Error!", 5000, 'red');
                                reveal.setErrorData(jqXHR.responseText);
                                reveal.state = 'error';
                                reveal.content.find('input.validate.valid').removeClass('valid').addClass('invalid');
                            }
                        });
                },
                setErrorData: function (error_data) {
                    response = $(error_data);
                    this.addContent(response);
                },
                setPostData: function () {
                    var error = false;
                    if (!this.post_data) {
                        return;
                    }
                    $.each($(this.post_data).find('.input-field'), function (a, b) {
                        var field = function () {
                            return form.find('.input-field:nth(' + a + ')')[0];
                        };
                        $(field()).replaceWith($(b));
                        if ($(b).find('.invalid')[0]) {
                            $(field()).parents('.todo-item').find('.activator').prop("checked", false);
                            error = true;
                        }
                    });

                    this.post_data = null;

                    // File Input Path
                    form.find('.file-field').each(function () {
                        var path_input = $(this).find('input.file-path');
                        $(this).find('input[type="file"]').change(function () {
                            path_input.val($(this)[0].files[0].name);
                            path_input.trigger('change');
                        });
                    });
                    form.find('.todo-item > .input-field, .todo-item > .input-group').addClass('hide')
                    form.find('select').material_select();
                },
                show: function () {
                    console.log(this.reveal);
                    this.reveal.css({display: 'block'}).velocity("stop", false).velocity({translateY: '-100%'}, {
                        duration: 300,
                        queue: false,
                        easing: 'easeInOutQuad'
                    });
                },
                unbindButtons: function () {
                    this.cancel_btn.unbind('click');
                    this.close_btn.unbind('click');
                    this.save_btn.unbind('click');

                },
            };
        reveal.init();

        form.submit(function (e) {
            e.preventDefault();
            reveal.save();
        });

        form.find('a[name=finish]').on('click', function (e) {
            e.preventDefault();
            $(this).off('click');

            form.find('input[name*=finish]').val(true)
            form.submit();


        });

        $(this).find('.activator').on('click', function (e) {
            var activator = this;
            e.preventDefault();

            /*
             setTimeout is important to identify the activator state
             */

            setTimeout(function () {
                reveal.target = activator;
                reveal.addContent();
                reveal.show();

            }, 100)
        });
        $('.input-field.hide:has(.valid), .input-group.hide .input-field:has(.valid)').prev().find('input[type=checkbox]').prop("checked", true);
        $('.input-group.hide>.input-field:has(.valid)').parent().prev().find('input[type=checkbox]').prop("checked", true);
    }
})(jQuery);

$(document).ready(function () {
    $('.fancybox').fancybox({
        'afterClose': function () {
            parent.location.reload(true);
        }
    });
    $.each($('form > .card.todo-list'), function () {
        $(this).todoList();
    });

})
