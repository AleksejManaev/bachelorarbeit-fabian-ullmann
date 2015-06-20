# -*- coding: utf-8 -*-
__author__ = 'ullmanfa'
from django.conf import settings

try:
    from importlib import import_module
except ImportError:
    from django.utils.importlib import import_module

# Default Settings

MATERIALIZE_DEFAULTS = {
    'material_css_url': '/static/css/material.css',
    'material_js_url': '/static/js/material.js',
    'materialize_form_todolist_js_url': '/static/js/material.todoform.js',
    'jquery_url': '//code.jquery.com/jquery-latest.min.js',
    'bootstrap_url': '/static/js/bootstrap.min.js',
    'jquery_ui_url': '//code.jquery.com/ui/1.11.4/jquery-ui.js',
    'jquery_ui_css_url': '//code.jquery.com/ui/1.11.4/themes/smoothness/jquery-ui.css',
    'jquery_offline': '/static/js/jquery-2.1.1.min.js',
    'materialize_css_url': '//cdnjs.cloudflare.com/ajax/libs/materialize/0.96.1/css/materialize.min.css',
    'materialize_css_offline': '/static/css/materialize.min.css',
    'materialize_js_url': '//cdnjs.cloudflare.com/ajax/libs/materialize/0.96.1/js/materialize.min.js',
    'materialize_js_offline': '/static/js/materialize.min.js',
    'pickadate_'
    'animate_url': '/static/vendors/animate-css/animate.min.css',
    'fancybox_js_url': '/static/vendors/fancybox/js/jquery.fancybox.pack.js?v=2.1.5',
    'fancybox_css_url': '/static/vendors/fancybox/css/jquery.fancybox.css?v=2.1.5',
    'login_js': '/static/js/material_pages/material_login_page.js',
    'offline_mode': False,
    'error_css_class': 'has-error',
    'javascript_in_head': False,
    'base_color_default': 'rgb(0, 0, 0)',
    'base_color': None,
    'set_placeholder': False,
    'form_renderers': {
        'default': 'materialize.renderers.FormRenderer',
        'todo': 'materialize.renderers.FormTodoRenderer',
    },
    'formset_renderers': {
        'default': 'materialize.renderers.FormsetRenderer',
        'todo': 'materialize.renderers.FormsetTodoRenderer',
    },
    'field_renderers': {
        'default': 'materialize.renderers.FieldRenderer',
        'inline': 'materialize.renderers.InlineFieldRenderer',
        'todo': 'materialize.renderers.TodoFieldRenderer',
    },
}


# Start with a clone of default settings

MATERIALIZE = MATERIALIZE_DEFAULTS.copy()

# Override with settings from settings.py

MATERIALIZE.update(getattr(settings, 'MATERIALIZE', {}))


def get_materialize_setting(setting, default=None):
    return MATERIALIZE.get(setting, default)


def material_css_url():
    return get_materialize_setting('material_css_url')


def material_js_url():
    return get_materialize_setting('material_js_url')


def materialize_css_url():
    return get_materialize_setting('materialize_css_url') if not get_materialize_setting(
        'offline_mode') else get_materialize_setting('materialize_css_offline')


def materialize_js_url():
    return get_materialize_setting('materialize_js_url') if not get_materialize_setting(
        'offline_mode') else get_materialize_setting('materialize_js_offline')


def material_form_todolist_js_url():
    return get_materialize_setting('materialize_form_todolist_js_url')


def jquery_url():
    return get_materialize_setting('jquery_url') if not get_materialize_setting(
        'offline_mode') else get_materialize_setting('jquery_offline')


def bootstrap_url():
    return get_materialize_setting('bootstrap_url')

def jquery_ui_url():
    return get_materialize_setting('jquery_ui_url')


def jquery_ui_css_url():
    return get_materialize_setting('jquery_ui_css_url')


# Todo jquery_ui_offline erstellen
def animate_css():
    return get_materialize_setting('animate_url')


def fancybox_css():
    return get_materialize_setting('fancybox_css_url')


def fancybox_js():
    return get_materialize_setting('fancybox_js_url')


def login_js():
    return get_materialize_setting('login_js')


def material_vars():
    dict = {}
    if get_materialize_setting('base_color'):
        dict['base_color'] = get_materialize_setting('base_color')
        dict['base_color_default'] = get_materialize_setting('base_color_default')
    return dict


def get_renderer(renderers, **kwargs):
    layout = kwargs.get('layout', '')
    path = renderers.get(layout, renderers[kwargs.get('type') if kwargs.get('type') else 'default'])
    mod, cls = path.rsplit(".", 1)
    return getattr(import_module(mod), cls)


def get_formset_renderer(**kwargs):
    renderers = get_materialize_setting('formset_renderers')
    return get_renderer(renderers, **kwargs)


def get_form_renderer(**kwargs):
    renderers = get_materialize_setting('form_renderers')
    return get_renderer(renderers, **kwargs)


def get_field_renderer(**kwargs):
    renderers = get_materialize_setting('field_renderers')
    return get_renderer(renderers, **kwargs)
