# -*- coding: utf-8 -*-
from django import template
from materialize.components import render_card_reveal, render_todo_item_begin, render_todo_item_end, \
    render_todo_item_activator
from materialize.render_form import *
from materialize.materialize import *

__author__ = 'ullmanfa'

register = template.Library()


@register.filter
def material_setting(value):
    return get_materialize_setting(value)


@register.simple_tag
def material_css():
    css = '<link href="{}" media="all" rel="stylesheet"></script>'.format(materialize_css_url())
    css += '<link href="{}" media="all" rel="stylesheet"></script>'.format(fancybox_css())
    css += '<link href="{}" media="all" rel="stylesheet"></script>'.format(material_css_url())
    return css


@register.simple_tag
def material_js(jquery=True):
    js = '<script type="text/javascript" src="{}"></script>'.format(jquery_url()) if jquery else ''
    js += '<script type="text/javascript" src="{}"></script>'.format(fancybox_js())
    js += '<script type="text/javascript" src="{}"></script>'.format(materialize_js_url())
    js += '<script type="text/javascript"src="{}"></script>'.format(material_js_url())
    return js


@register.simple_tag
def meterial_animate_css():
    return '<link href="{}" media="all" rel="stylesheet"></script>'.format(animate_css())


@register.simple_tag
def material_login_js():
    return '<script src="{}"></script>'.format(login_js())


@register.simple_tag
def material_action_dropdown(target):
    action = '<div class="actions dropdown-button" data-activates="'
    action += target
    action += '"><a href="#!"><i class="mdi-navigation-more-vert"></i></a></div>'
    return action


@register.simple_tag
def material_form(*args, **kwargs):
    return render_form(*args, **kwargs)


@register.simple_tag
def material_formfield(*args, **kwargs):
    return render_field(*args, **kwargs)


@register.simple_tag
def material_formset(*args, **kwargs):
    return render_formset(*args, **kwargs)


@register.simple_tag
def material_form_errors(*args, **kwargs):
    return render_form_errors(*args, **kwargs)


@register.simple_tag
def material_block_header(title='', action_visibility=False):
    actions = ''
    if action_visibility:
        actions += '<li><a href=""><i class="mdi-action-visibility-off"></i></a></li>'

    return '<div class="block-header"><h2 class="left">{title}</h2>' \
           '<ul class="actions right">{actions}' \
           '</ul></div>'.format(title=title, actions=actions)


@register.simple_tag
def material_divider():
    return '<div class="divider"></div>'


@register.simple_tag
def material_card_header(title='', actions=None):
    card_header = '<div class="card-header">'
    card_header += '<div class="card-title blue-grey-text">'
    card_header += title
    card_header += material_action_dropdown(actions) if actions else ''
    card_header += '</div>'
    card_header += '</div>'
    return card_header


@register.simple_tag
def material_card_action(action_text='submit'):
    card_action = '<div class="card-action valign-wrapper"><a class="col s12 center-align">'
    card_action += action_text
    card_action += '</a></div>'
    return card_action


@register.simple_tag
def material_todo_form(*args, **kwargs):
    kwargs['layout'] = 'todo'
    return render_form(*args, **kwargs)


@register.simple_tag
def material_todo_formfields(*args, **kwargs):
    kwargs['layout'] = 'todo'
    return render_formfields(*args, **kwargs)


@register.simple_tag
def material_todo_formsetfields(*args, **kwargs):
    kwargs['layout'] = 'todo'
    return render_formsetfields(*args, **kwargs)


@register.simple_tag
def material_todo_formfield(*args, **kwargs):
    kwargs['layout'] = 'todo'
    return render_field(*args, **kwargs)


@register.simple_tag
def material_todo_js():
    return '<script src="{}"></script>'.format(material_form_todolist_js_url())


@register.simple_tag
def material_todo_formset(*args, **kwargs):
    kwargs['layout'] = 'todo'
    return render_formset(*args, **kwargs)


@register.simple_tag
def material_todo_reveal(*args, **kwargs):
    return render_card_reveal()


@register.simple_tag
def material_todo_item_begin(*args, **kwargs):
    return render_todo_item_begin()


@register.simple_tag
def material_todo_item_end(*args, **kwargs):
    return render_todo_item_end()


@register.simple_tag
def material_todo_item_activator(*args, **kwargs):
    return render_todo_item_activator(kwargs.get('id', 'id_todo'), kwargs.get('label', 'Activator'))
