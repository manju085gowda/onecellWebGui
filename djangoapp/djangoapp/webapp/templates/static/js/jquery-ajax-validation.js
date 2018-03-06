(function($) {
    function inputs(form)   {
        return form.find(":input:visible:not(:button)");
    }
    $.fn.validate = function(url, settings) {
        settings = $.extend({
            callback: false,
            fields: true,
            event: 'change',
            submitHandler: null,
            fieldSuccessCallback: null,
            formSuccessCallback: null,
            fieldInvalidCallback: null,
            callback: null
        }, settings);

        function ajaxForm(form, data, field, formSuccessCallback) {
            var field = field || false;
            var formSuccessCallback = formSuccessCallback || false;
            $.ajax({
                async: true,
                data: data,
                dataType: 'json',
                traditional: true,
                error: function(XHR, textStatus, errorThrown)   {
                    status = true;
                },
                success: function(data, textStatus) {
                    status = data.valid;
                    if (data.valid) {     
                        if(settings.fieldSuccessCallback) {
                            settings.fieldSuccessCallback($('#' + field));
                        }
                        $(form).find('div.errorlist').hide();
                        //$('#' + field).removeClass('fieldError');
                        $(form).find('input').removeClass('fieldError');
                        if(settings.formSuccessCallback) {
                            settings.formSuccessCallback($(form));
                        }
                    } else {
                        if (settings.callback)  {
                            settings.callback($(form), data);
                        }
                        else    {
                            var get_form_error_position = function(key) {
                                key = key || '__all__';
                                if (key == '__all__') {
                                    var filter = ':first';
                                } else {
                                    var filter = ':first[id^=id_' + key.replace('__all__', '') + ']';
                                }
                                return inputs(form).filter(filter).parent();
                            };
                                if(!data.errors[field]  && settings.fieldSuccessCallback) {
                                    if($('#'+field).attr('class').search('mutator') !== -1)
                                    {
                                        $(form).find('div.errorlist').show();
                                        $.each(data.errors, function(key, val)  {
                                            $(form).find('#' + key).addClass('fieldError');
                                    });
                                      settings.fieldInvalidCallback($('#' + field));
                                    }
                                    else
                                    {
                                    $('#' + field).next('div.errorlist').remove();
                                    settings.fieldSuccessCallback($('#' + field));
                                    $('#' + field).removeClass('fieldError');
                                    }
                                }
                                $.each(data.errors, function(key, val)  {
                                    if (key.indexOf('__all__') >= 0)   {
                                        var error = get_form_error_position(key);
                                        if (error.prev().is('ul.errorlist')) {
                                            error.prev().before('<div class="wizard-error errorlist">' + val + '</div>');
                                        }
                                    }
                                    else {
                                        if(field) {
                                            if(field == key && $('#' + field).val().length >= 0) {
                                                if(settings.fieldInvalidCallback) {
                                                    settings.fieldInvalidCallback($('#' + field));
                                                }
                                                $('#' + field).next('div.errorlist').remove();
                                                $('#' + key).after('<div class="wizard-error errorlist">' + val + '</div>');
                                                $('#' + field).addClass('fieldError');
                                            }
                                        } else {
                                            if(settings.fieldInvalidCallback) {
                                                settings.fieldInvalidCallback($('#' + field));
                                            }
                                            $('#' + field).next('div.errorlist').remove();
                                            $('#' + key).after('<div class="wizard-error errorlist">' + val + '</div>');
                                            $('#' + field).addClass('fieldError');
                                        }
                                    }
                                });
                        }
                    }
                },
                type: 'POST',
                url: url
            });
        }


        if(settings.event != 'submit') {
            if(Object.prototype.toString.call(settings.fields)  == '[object Array]') {
                var form = $(this);
                $(settings.fields).each(function(i,el) {
                    $('#' + el).each(function(index, el) {
                        $(el).on(settings.event, function(event) {
                            field = $(this).attr("id");
                            ajaxForm($(form), $(form).serialize(), field, null);
                        });
                    });
                });
            } else {
                var form = $(this);
                $('input, checkbox, select, textarea',this).not('input[type=submit]').each(function(index, el) {
                    $(el).on(settings.event, function(event) {
                        field = $(this).attr("id");
                        ajaxForm($(form), $(form).serialize(), field, null);
                    });
                });
            }
        } 

        /*$(this).on("submit", function(event) {
            event.preventDefault();
            $(this).find('label.errorlist').remove();
            ajaxForm($(this), $(this).serialize()+"&submit=true", null, settings.formSuccessCallback);
        });*/
    };
})(jQuery);
