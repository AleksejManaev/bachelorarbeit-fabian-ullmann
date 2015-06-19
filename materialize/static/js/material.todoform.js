/**
 * Created by ullmanfa on 17.05.15.
 */

(function ($) {
    //Todo Error-Meldungen optimieren
    //Todo Aktualisierung überprüfen
    $.fn.todoList = function () {

        $(document).off('click.card', '.card');
        var _this = this,
            form = {
                instance: $(_this).parent(),
                init: function () {
                    this.instance.submit(function (e) {
                        e.preventDefault();
                    });
                    this.instance.find('.activator').on('click', function (e) {
                        var activator = this;
                        e.preventDefault();

                        /*
                         setTimeout is important to identify the activator state
                         */
                        setTimeout(function () {
                            reveal.target = activator;
                            reveal.addContent();
                            reveal.show();

                        }, 200)
                    });
                    $('.input-field.hide:has(.valid)').prev().find('input[type=checkbox]').prop("checked", true);
                    $('.input-group.hide>.input-field:has(.valid)').parent().prev().find('input[type=checkbox]').prop("checked", true);

                    $(this.instance).find('.card-action [name=finish], .card-action [name=pdf]').off('click');
                    $(this.instance).find('.card-action [name=finish]').on('click', function () {
                        form.saveFinal();
                    });
                    $(this.instance).find('.card-action [name=pdf]').on('click', function (e) {
                        form.savePDF(e);
                        return false;
                    });
                },
                getPostData: function () {
                    var postData = new FormData(),
                        mainData = this.instance.serializeArray(),
                        input = reveal.content.find('input[id], textarea[id], select[id]');

                    $.each(mainData, function (key, input) {
                        postData.append(input.name, input.value);
                    });
                    $.each(input, function (i, inp) {
                        if (input[i].files) {
                            $.each(input[i].files, function (i, file) {
                                postData.append($(input[i]).attr('name'), file);
                            })
                        }
                    });
                    return postData;
                },
                refresh: function () {

                    if ($('select')[0]) {
                        $('select').material_select();
                    }
                    // File Input Path
                    $('.file-field').each(function () {
                        var path_input = $(this).find('input.file-path');
                        $(this).find('input[type="file"]').change(function () {
                            path_input.val($(this)[0].files[0].name);
                            path_input.trigger('change');
                        });
                    });
                },
                sendForm: function (postData, success, error) {
                    $.ajax(
                        {
                            url: form.instance.attr('action'),
                            data: postData,
                            cache: false,
                            contentType: false,
                            processData: false,
                            type: 'POST',
                            success: success,
                            error: error,
                        });
                },
                savePDF: function (e) {
                    // Todo onSuccess Finish-Button entfernen und actions aktualisieren
                    var postData = this.getPostData();
                    this.sendForm(
                        postData,
                        function (data, textStatus, jqXHR) {
                            //data: return data from server
                            Materialize.toast("pdf generated", 2000, 'green');
                            window.location.href = e.target.href;
                        },
                        function (jqXHR, textStatus, errorThrown) {
                            Materialize.toast("pdf not generated!", 5000, 'red');
                        });
                },
                saveSubmit: function () {
                    var postData = this.getPostData();
                    this.sendForm(
                        postData,
                        function (data, textStatus, jqXHR) {
                            //data: return data from server
                            Materialize.toast("finished", 2000, 'green');
                            form.setFinalSuccessData();
                        },
                        function (jqXHR, textStatus, errorThrown) {
                            Materialize.toast("Not finished!", 5000, 'red');
                            form.setFinalErrorData(jqXHR.responseText);

                        });
                },
                saveFinal: function () {
                    // Todo onSuccess Finish-Button entfernen und actions aktualisieren
                    form.instance.find('input[name*=finished]').val('True');
                    var postData = this.getPostData();
                    postData.append('finalize', true);
                    this.sendForm(
                        postData,
                        function (data, textStatus, jqXHR) {
                            //data: return data from server
                            Materialize.toast("finished", 2000, 'green');
                            form.setFinalSuccessData();
                            window.location.reload();
                        },
                        function (jqXHR, textStatus, errorThrown) {
                            Materialize.toast("Not finished!", 5000, 'red');
                            form.setFinalErrorData(jqXHR.responseText);

                        });
                },
                saveReveal: function () {
                    var target_forms = [],
                        postData = this.getPostData();
                    $.each($(reveal.input), function (i, inp) {
                        var str = String($(inp).attr('name')).split('-')[0];
                        if (str != 'undefined' && target_forms.indexOf(str) < 0) {
                            target_forms.push(str);
                        }
                    });
                    reveal.target_forms = target_forms;
                    postData.append('target_form', target_forms);
                    this.sendForm(
                        postData,
                        function (data, textStatus, jqXHR) {
                            //data: return data from server
                            Materialize.toast("saved", 2000, 'green');
                            reveal.post_data = data;
                            reveal.state = 'saved';
                            form.setPostData(jqXHR.responseText);
                            reveal.hide();
                        },
                        function (jqXHR, textStatus, errorThrown) {
                            Materialize.toast("Input Error!", 5000, 'red');
                            reveal.state = 'error';
                            reveal.content.find('input.validate.valid').removeClass('valid').addClass('invalid');
                            form.setPostData(jqXHR.responseText);

                        });

                },
                setPostData: function (post_data) {
                    response = $(post_data);
                    $.each(response.find('input[id], textarea[id], select[id]'), function (a, b) {
                        var name = $(b).attr('name') ? $(b).attr('name') : '';
                        if ($.inArray(name.split('-')[0], reveal.target_forms) >= 0) {
                            var tmp = "#id_" + name;
                            if ($(b).parents('.input-field').length > 0 && $(reveal.content).find(tmp).length > 0) {
                                $($(reveal.content).find(tmp).parents('.input-field')[0]).replaceWith($($(b).parents('.input-field')[0]).removeClass('hide'));

                            } else {
                                $(reveal.content).find(tmp).replaceWith($(b));
                            }
                        }
                    });
                    form.refresh();
                    reveal.setContentHeight();

                },
                setFinalErrorData: function (post_data) {
                    response = $(post_data);
                    $.each(response.find('input[id], textarea[id], select[id]'), function (a, b) {
                        var name = $(b).attr('name') ? $(b).attr('name') : '';
                        var tmp = "#id_" + name;
                        if ($(b).parents('.input-field').length > 0 && form.instance.find(tmp).length > 0) {
                            var tmp = $(form.instance.find(tmp).parents('.input-field')[0]),
                                tmp_classes = tmp.attr('class');
                            tmp.replaceWith($($(b).parents('.input-field')[0]).addClass(tmp_classes));
                        } else {
                            form.instance.find(tmp).replaceWith($(b));
                        }

                        form.instance.find('.red-text').parents('.todo-item').find('label').removeClass('red-text');
                        form.instance.find('.has-error, .invalid').parents('.todo-item').find('label').addClass('red-text');
                        form.refresh();
                    });
                },
                setFinalSuccessData: function () {
                    $.ajax({
                            url: parent.location.href,
                            method: 'GET',
                            success: function (data, textStatus, jqXHR) {
                                var response = jqXHR.responseText,
                                    action = form.instance.attr('action');
                                form.instance.replaceWith($($(response).find('[action="' + action + '"]')[0]));
                                $.removeData(_this.todoList);
                                $.each($('form[action="' + action + '"] > .card.todo-list'), function () {
                                    $(this).todoList();
                                });
                            }
                        }
                    )
                },
                showErrors: function () {
                    //Todo Error-Meldungen optimieren
                }
            },
            reveal = {

                addContent: function (from) {
                    var _from = from || _this;
                    var inp_target = $(_from).find('#' + $(this.target).attr('id').replace('_todo', '')).parents('.input-field.hide');

                    if (!inp_target[0]) {
                        inp_target = $(this.target).parents('.todo-item').find('.input-group.hide')
                    }

                    $(this.title).text($(this.target).parent().find('label').text());
                    $(this.title).append(this.close_btn);
                    $(this.content).html(inp_target.removeClass('hide'));
                    $(this.instance).show();
                    this.input = $(this.instance).find('input, textarea, select');
                    this.input_original = this.input.clone();
                    this.state = '';

                    if (this.target.indeterminate) {
                        this.state = 'changed'
                    }
                    ;
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
                        if (reveal.state == 'changed' || reveal.state == 'error') {
                            form.saveReveal();
                        } else {
                            reveal.hide();
                        }
                    });
                },
                cancel: function () {
                    $.ajax({
                        url: form.instance.attr('action'),
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
                            reveal.setContentHeight()
                            //setContentHeight(_this, reveal.content);
                        }, 300);
                    });
                    $(this.input).on('change', function () {
                        reveal.state = 'changed';
                        $(this).off('change');
                    });

                    reveal.setContentHeight();
                },
                hide: function () {
                    $(this.instance).velocity("stop", false).velocity(
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
                    this.instance = $(_this).find('.card-reveal');
                    this.title = this.instance.find('.card-title');
                    this.content = this.instance.find('.card-content');
                    this.close_btn = this.instance.find('.card-title i');
                    this.cancel_btn = this.instance.find('.card-action a[data-cr-action=dismiss]');
                    this.save_btn = this.instance.find('.card-action a[data-cr-action=save]');
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
                                && (!$(this.content).find('input[id$="clear_id"]:checked')[0] && !$(this.content).find('input[id$="DELETE"]:checked')[0])
                                && !Boolean(Boolean($(this.content).find('option:selected')[0])
                                    && !Boolean($(this.content).find('option:selected').val()))) {
                                target.find('.activator').prop("checked", true);
                                target.find('label').removeClass('red-text');
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
                    this.setContentHeight();
                },
                setContentHeight: function () {
                    var my_height = $(this.content).outerHeight(),
                        parent_height = $(_this).find('> .card-content').height();

                    if (my_height > parent_height) {
                        $(_this).find('> .card-content').first().css({'height': $(this.content).outerHeight()});
                    } else {
                        $(_this).find('> .card-content').first().css({'height': $(this.content).css('min-height')});
                    }
                },
                show: function () {
                    this.instance.css({display: 'block'}).velocity("stop", false).velocity({translateY: '-100%'}, {
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


        form.init();
        reveal.init();

        if ($('select')[0]) {
            $('select').material_select();
        }
        ;
        //

    }
})(jQuery);

$(document).ready(function () {
    if ($('.card-reveal')[0]) {
        $('.card-reveal').show();
        $.each($('.card-reveal .card-content'), function (a, b) {
            $(b).css('min-height', $(b).parent().outerHeight() - $(b).parent().find('.card-header').outerHeight() - $(b).parent().find('.card-action').outerHeight());
        });
        $('.card-reveal').hide();
    }
    $.each($('form > .card.todo-list'), function () {
        $(this).todoList();
    });

})
