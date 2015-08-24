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
    """
    Gibt alle HTML-Link-Tags aus, die für die korrekte Darstellung notwendig sind.
    :return:
    """
    css = '<link href="{}" media="all" rel="stylesheet"></script>'.format(materialize_css_url())
    css += '<link href="{}" media="all" rel="stylesheet"></script>'.format(fancybox_css())
    css += '<link href="{}" media="all" rel="stylesheet"></script>'.format(material_css_url())
    return css


@register.simple_tag
def material_js(jquery=True):
    """
    Gibt HTML-Code aus, mit dem alle benötigten JavaScript-Dateien in
    korrekter Reihenfolge geladen werden können.
    :param jquery:
    :return:
    """
    js = '<script type="text/javascript" src="{}"></script>'.format(jquery_url()) if jquery else ''
    js += '<script type="text/javascript" src="{}"></script>'.format(bootstrap_url())
    js += '<script type="text/javascript" src="{}"></script>'.format(materialize_js_url())
    js += '<script type="text/javascript" src="{}"></script>'.format(fancybox_js())
    js += '<script type="text/javascript"src="{}"></script>'.format(material_js_url())
    return js


@register.simple_tag
def material_login_js():
    """
    Gibt einzelnen HTML-Code zum Laden der Login-JavaScript-Datei aus.
    Ist in material_js() nicht integriert, da die Datei nur auf Login-Seiten
    benötigt wird.
    :return:
    """
    return '<script src="{}"></script>'.format(login_js())


@register.simple_tag
def material_action_dropdown(target):
    """
    Rendert einen div-Block, der eine Schaltfläche beinhaltet,
    mit der das unter target angegebene Menü geöffnet werden kann.
    :param target:
    :return:
    """
    action = '<div class="actions dropdown-button" data-activates="'
    action += target
    action += '"><a href="#!"><i class="mdi-navigation-more-vert"></i></a></div>'
    return action


@register.simple_tag
def material_form(*args, **kwargs):
    """
    Rendert ein Django-Formular, welches über den Parameter form anzugeben ist.
    Das Rendering wird materialize.renderers.FormRenderer übernommen.
    :param args:
    :param kwargs:
    :return:
    """
    return render_form(*args, **kwargs)


@register.simple_tag
def material_formfield(*args, **kwargs):
    """
    Rendert ein einzelnes Django-Formularfeld, das mit den Parameter field übergeben wird.
    Durch Verwendung des zweiten Parameters kann dem Feld ein Icon hinzugefügt werden.
    Rendering wird von materialize.renderers.FormField übernommen.
    :param args:
    :param kwargs:
    :return:
    """
    return render_field(*args, **kwargs)


@register.simple_tag
def material_formset(*args, **kwargs):
    """
    Rendert ein Django-Formset, das mit den Parameter formset übergeben wird.
    Rendering wird von materialize.renderers.Formset übernommen.
    :param args:
    :param kwargs:
    :return:
    """
    return render_formset(*args, **kwargs)


@register.simple_tag
def material_divider():
    """
    Rendert eine horizontale Trennline.
    :return:
    """
    return '<div class="divider"></div>'


@register.simple_tag
def material_card_header(title='', actions=None):
    """
    Rendert den Kopfbereich einer Card.
    Anzuzeigender Titel und mögliche Aktionen können angegeben werden.
    :param title:
    :param actions:
    :return:
    """
    card_header = '<div class="card-header">'
    card_header += '<div class="card-title blue-grey-text">'
    card_header += title
    card_header += material_action_dropdown(actions) if actions else ''
    card_header += '</div>'
    card_header += '</div>'
    return card_header


@register.simple_tag
def material_card_action(action_text='submit'):
    """
    Rendert eine Schaltfläche für den Aktion-Bereich einer Card.
    :param action_text:
    :return:
    """
    card_action = '<div class="card-action valign-wrapper"><a class="col s12 center-align">'
    card_action += action_text
    card_action += '</a></div>'
    return card_action


@register.simple_tag
def material_todo_form(*args, **kwargs):
    """
    Rendert ein Django-Formular als Todo-Liste. Über den Parameter form ist das Formular anzugeben.
    Das Rendering wird materialize.renderers.FormTodoRenderer übernommen.
    :param args:
    :param kwargs:
    :return:
    """
    kwargs['layout'] = 'todo'
    return render_form(*args, **kwargs)


@register.simple_tag
def material_todo_formfields(*args, **kwargs):
    """
    Rendert ein Django-Formular als Todo-Items, welches mit dem Parameter form angegeben wird.
    Das Rendering wird materialize.renderers.FormRenderer übernommen.
    :param args:
    :param kwargs:
    :return:
    """
    kwargs['layout'] = 'todo'
    return render_formfields(*args, **kwargs)


@register.simple_tag
def material_todo_formsetfields(*args, **kwargs):
    """
    Rendert ein Django-Formular als Todo-Items, welches mit dem Parameter form angegeben wird.
    Das Rendering wird materialize.renderers.FormTodoRenderer übernommen.
    :param args:
    :param kwargs:
    :return:
    """
    kwargs['layout'] = 'todo'
    return render_formsetfields(*args, **kwargs)


@register.simple_tag
def material_todo_formfield(*args, **kwargs):
    """
    Rendert ein einzelnes Django-Formularfeld als Todo-Item, das mit dem Parameter
    field übergeben wird. Durch Verwendung des zweiten Parameters kann dem Feld ein
    Icon hinzugefügt werden. Rendering wird von materialize.renderers.TodoFieldRenderer übernommen.
    :param args:
    :param kwargs:
    :return:
    """
    kwargs['layout'] = 'todo'
    return render_field(*args, **kwargs)


@register.simple_tag
def material_todo_js():
    """
    Gibt einzelnen HTML-Code zum Laden der Todo-JavaScript-Datei aus. Ist in material_js()
    nicht integriert, da die Datei nur auf Todo-Seiten benötigt wird.
    :return:
    """
    return '<script src="{}"></script>'.format(material_form_todolist_js_url())


@register.simple_tag
def material_todo_formset(*args, **kwargs):
    """
    Rendert ein Django-Formset als Todo-Items, welches mit dem Parameter formset angegeben wird.
    Das Rendering wird materialize.renderers.FormsetTodoRenderer übernommen.
    :param args:
    :param kwargs:
    :return:
    """
    kwargs['layout'] = 'todo'
    return render_formset(*args, **kwargs)


@register.simple_tag
def material_todo_reveal(*args, **kwargs):
    """
    Rendert eine Overlay-Komponente in der ein Todo-Item angezeigt wird, nachdem ein Aktivator betätigt wurde.
    :param args:
    :param kwargs:
    :return:
    """
    return render_card_reveal()


@register.simple_tag
def material_todo_item_begin(*args, **kwargs):
    """
    Gibt die öffnenden Tags für ein Todo-Item zurück.
    :param args:
    :param kwargs:
    :return:
    """
    return render_todo_item_begin()


@register.simple_tag
def material_todo_item_end(*args, **kwargs):
    """
    Gibt die schließenden Tags für ein Todo-Item zurück.
    :param args:
    :param kwargs:
    :return:
    """
    return render_todo_item_end()


@register.simple_tag
def material_todo_item_activator(*args, **kwargs):
    """
    Rendert einen div-Block, der eine Input-Feld enthält mit dem durch Betätigung ein Todo-Item,
    welches über den Parameter id adressiert wird, aktiviert werden kann. Mit dem zweiten Parameter
    label kann die Beschreibung für den Aktivator angegeben werden.
    :param args:
    :param kwargs:
    :return:
    """
    return render_todo_item_activator(kwargs.get('id', 'id_todo'), kwargs.get('label', 'Activator'))
