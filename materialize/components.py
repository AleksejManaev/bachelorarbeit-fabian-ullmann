# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.forms.widgets import flatatt

from .text import text_value


def render_icon(icon, title='', classes=''):
    """
    Render a Material Design Icon
    """
    attrs = {
        'class': 'mdi-{icon} {klass}'.format(icon=icon, klass=classes),
    }
    if title:
        attrs['title'] = title
    return '<i{attrs}></i>'.format(attrs=flatatt(attrs))


def render_modal(content, modal_type=None, dismissable=True):
    # Todo footer berücksichtigen
    """
    Render a Material modal
    """
    button = ''
    footer = ''
    css_classes = ['modal']
    if modal_type:
        css_classes.append('modal-' + text_value(modal_type))

    if dismissable:
        css_classes.append('modal-dismissable')
        button = '<i class="mdi-navigation-close right"></i>'
    return '<div class="{css_classes}">{button}<div class="modal-content">{content}</div>' \
           '<div class="modal-footer">' \
           '<a href="#!" class=" modal-action modal-close waves-effect waves-green btn-flat">Agree</a>' \
           '</div>'.format(
        css_classes=' '.join(css_classes),
        button=button,
        content=text_value(content),
    )


def render_card_reveal():
    return '<div class="card-reveal">' \
           '<div class="card-header">' \
           '<span class="card-title blue-grey-text">Card Title ' \
           '<i class="mdi-navigation-close right"></i>' \
           '</span>' \
           '</div>' \
           '<div class="card-content valign-wrapper"></div>' \
           '<div class="card-action">' \
           '<a href="" data-cr-action="dismiss">' \
           '<i class="mdi-navigation-close red-text"></i>' \
           '</a>' \
           '<a href="" data-cr-action="save">' \
           '<i class="mdi-navigation-check green-text"></i>' \
           '</a>' \
           '</div>' \
           '</div>'


def render_todo_item_begin():
    return '<div class="todo-item valign-wrapper row">'


def render_todo_item_end():
    return '</div>'


def render_todo_item_activator(id, label):
    return '<div class="col s12">' \
           '<input type="checkbox" class="activator" id="{id}">' \
           '<label for="{id}">{label}</label>' \
           '</div>'.format(id=id, label=label)
