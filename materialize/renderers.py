# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.forms import ReadOnlyPasswordHashWidget
from bs4 import BeautifulSoup
from django.forms import (
    DateInput, ClearableFileInput, RadioSelect, NumberInput, Select)
from .forms.widgets import SelectAddNew
from django.forms.extras import SelectDateWidget
from django.forms.forms import BaseForm, BoundField
from django.forms.formsets import BaseFormSet
from django.utils.html import conditional_escape, strip_tags
from django.template import Context
from django.template.loader import get_template
from django.utils.safestring import mark_safe

from .components import render_card_reveal, render_todo_item_begin, render_todo_item_end, render_todo_item_activator
from .templatetags.material import material_card_header, material_card_action
from .render_form import *


class BaseRenderer(object):
    def __init__(self, *args, **kwargs):
        self.layout = kwargs.get('layout', '')
        self.form_group_class = kwargs.get(
            'form_group_class', FORM_GROUP_CLASS)
        self.item_group_class = kwargs.get(
            'item_group_class', ITEM_GROUP_CLASS)
        self.field_class = kwargs.get('field_class', '')
        self.label_class = kwargs.get('field_class', '')
        self.show_help = kwargs.get('show_help', True)
        self.show_label = kwargs.get('show_label', True)
        self.exclude = kwargs.get('exclude', '')
        self.set_required = kwargs.get('set_required', True)
        self.set_disabled = kwargs.get('set_disabled', False)
        self.size = self.parse_size(kwargs.get('size', ''))
        self.horizontal_label_class = kwargs.get(
            'horizontal_label_class',
            get_materialize_setting('horizontal_label_class')
        )
        self.horizontal_field_class = kwargs.get(
            'horizontal_field_class',
            get_materialize_setting('horizontal_field_class')
        )

    def parse_size(self, size):
        size = text_value(size).lower().strip()
        if size in ('sm', 'small'):
            return 'small'
        if size in ('lg', 'large'):
            return 'large'
        if size in ('md', 'medium', ''):
            return 'medium'
        raise MaterializeError('Invalid value "%s" for parameter "size" (expected "sm", "md", "lg" or "").' % size)

    def get_size_class(self, prefix='input'):
        if self.size == 'small':
            return prefix + '-sm'
        if self.size == 'large':
            return prefix + '-lg'
        return ''


class FormsetRenderer(BaseRenderer):
    """
    Default formset renderer
    """

    def __init__(self, formset, *args, **kwargs):
        if not isinstance(formset, BaseFormSet):
            raise MaterializeError(
                'Parameter "formset" should contain a valid Django Formset.')
        self.formset = formset
        self.reveal = kwargs.get('reveal', False)
        super(FormsetRenderer, self).__init__(*args, **kwargs)

    def render_management_form(self):
        return text_value(self.formset.management_form)

    def render_form(self, form, **kwargs):
        return render_form(form, **kwargs)

    def render_forms(self):
        rendered_forms = []
        for form in self.formset.forms:
            rendered_forms.append(self.render_form(
                form,
                reveal=self.reveal,
                layout=self.layout,
                form_group_class=self.form_group_class,
                field_class=self.field_class,
                label_class=self.label_class,
                show_label=self.show_label,
                show_help=self.show_help,
                exclude=self.exclude,
                set_required=self.set_required,
                set_disabled=self.set_disabled,
                size=self.size,
                horizontal_label_class=self.horizontal_label_class,
                horizontal_field_class=self.horizontal_field_class,
            ))
        return '\n'.join(rendered_forms)

    def render_formfields(self):
        rendered_forms = []
        for form in self.formset.forms:
            rendered_forms.append(render_formfields(
                form,
                reveal=self.reveal,
                layout=self.layout,
                form_group_class=self.form_group_class,
                field_class=self.field_class,
                label_class=self.label_class,
                show_label=self.show_label,
                show_help=self.show_help,
                exclude=self.exclude,
                set_required=self.set_required,
                set_disabled=self.set_disabled,
                size=self.size,
                horizontal_label_class=self.horizontal_label_class,
                horizontal_field_class=self.horizontal_field_class,
            ))
        return '\n'.join(rendered_forms)

    def get_formset_errors(self):
        return self.formset.non_form_errors()

    def render_errors(self):
        formset_errors = self.get_formset_errors()
        if formset_errors:
            return get_template(
                'material_form_errors.html').render(
                Context({
                    'errors': formset_errors,
                    'form': self.formset,
                    'layout': self.layout,
                })
            )
        return ''

    def render_fields(self):
        return self.render_errors() + self.render_management_form() + \
               self.render_formfields()

    def render(self):
        return self.render_errors() + self.render_management_form() + \
               self.render_forms()


class FormsetTodoRenderer(FormsetRenderer):
    def __init__(self, formset, *args, **kwargs):
        self.in_item_group = kwargs.get('item_group', 'False')
        super(FormsetTodoRenderer, self).__init__(formset, *args, **kwargs)

    def render_fields(self):
        main = super(FormsetTodoRenderer, self).render_fields()
        pre = post = ''
        if self.in_item_group:
            pre = '<div class={}>'.format(self.item_group_class)
            post = '</div>'
        return '{pre}{main}{post}'.format(pre=pre, main=main, post=post)


class FormRenderer(BaseRenderer):
    """
    Default form renderer
    """

    def __init__(self, form, *args, **kwargs):
        if not isinstance(form, BaseForm):
            raise MaterializeError(
                'Parameter "form" should contain a valid Django Form.')
        self.form = form
        self.formset = kwargs.get('formset', None)
        self.item_group = kwargs.get('item_group', False)
        super(FormRenderer, self).__init__(*args, **kwargs)
        # Handle form.empty_permitted
        if self.form.empty_permitted:
            self.set_required = False

    def render_fields(self):
        rendered_fields = []
        for field in self.form:
            rendered_fields.append(render_field(
                field,
                layout=self.layout,
                item_group=self.item_group,
                form_group_class=self.form_group_class,
                field_class=self.field_class,
                label_class=self.label_class,
                show_label=self.show_label,
                show_help=self.show_help,
                exclude=self.exclude,
                set_required=self.set_required,
                set_disabled=self.set_disabled,
                size=self.size,
                horizontal_label_class=self.horizontal_label_class,
                horizontal_field_class=self.horizontal_field_class,
            ))
        return '\n'.join(rendered_fields)

    def get_fields_errors(self):
        form_errors = []
        for field in self.form:
            if field.is_hidden and field.errors:
                form_errors += field.errors
        return form_errors

    def render_errors(self, type='all'):
        form_errors = None
        if type == 'all':
            form_errors = self.get_fields_errors() + \
                          self.form.non_field_errors()
        elif type == 'fields':
            form_errors = self.get_fields_errors()
        elif type == 'non_fields':
            form_errors = self.form.non_field_errors()

        if form_errors:
            return get_template(
                'material_form_errors.html').render(
                Context({
                    'errors': form_errors,
                    'form': self.form,
                    'layout': self.layout,
                })
            )
        return ''

    def render(self):
        return self.render_errors() + self.render_fields()


class MixedClassMeta(type):
    def __new__(cls, name, bases, classdict):
        classinit = classdict.get('__init__')  # could be None
        # define an __init__ function for the new class
        def __init__(self, *args, **kwargs):
            # call the __init__ functions of all the bases
            for base in type(self).__bases__:
                base.__init__(self, *args, **kwargs)
            # also call any __init__ function that was in the new class
            if classinit:  classinit(self, *args, **kwargs)

        # add the local function to the new class
        classdict['__init__'] = __init__
        return type.__new__(cls, name, bases, classdict)


class CardRenderer(object):
    # Todo Mehrere card_actions ermöglichen

    def __init__(self, form, *args, **kwargs):
        self.with_card = kwargs.get('with_card', True)
        self.title = kwargs.get('title', None)
        self.header_actions = kwargs.get('header_actions', None)
        self.card_actions = kwargs.get('card_actions', None)
        self.class_name = kwargs.get('class_name', None)

    def render_card(self, content):
        card = '<div class="card todo-list">'
        card += material_card_header(self.title, self.header_actions) if self.title else ''
        card += content
        card += material_card_action(self.card_actions) if self.card_actions else ''
        card += '</div>'
        return card


class FormTodoRenderer(FormRenderer, CardRenderer):
    __metaclass__ = MixedClassMeta  # important

    def __init__(self, form, *args, **kwargs):
        self.class_name = kwargs.get('class_name', None)
        super(FormTodoRenderer, self).__init__(form, *args, **kwargs)
        self.reveal = kwargs.get('reveal', True)

    def render(self):
        pre = '<div class={class_name}>'.format(class_name=self.class_name) if self.class_name else ''
        post = '</div>'
        post += render_card_reveal() if self.reveal else ''
        content = '{pre}{main}{post}'.format(pre=pre, post=post, main=super(FormTodoRenderer, self).render())

        return content if not self.with_card else self.render_card(content)


class FieldRenderer(BaseRenderer):
    """
    Default field renderer
    """

    def __init__(self, field, *args, **kwargs):
        if not isinstance(field, BoundField):
            raise MaterializeError(
                'Parameter "field" should contain a valid Django BoundField.')
        self.field = field
        super(FieldRenderer, self).__init__(*args, **kwargs)
        self.widget = field.field.widget
        self.initial_attrs = self.widget.attrs.copy()
        self.field_help = text_value(mark_safe(field.help_text)) \
            if self.show_help and field.help_text else ''
        self.field_errors = [conditional_escape(text_value(error))
                             for error in field.errors]
        self.in_group = kwargs.get('item_group', False)
        if get_materialize_setting('set_placeholder'):
            self.placeholder = field.label
        else:
            self.placeholder = ''

        self.addon_before = kwargs.get('addon_before', self.initial_attrs.pop('addon_before', ''))
        self.addon_after = kwargs.get('addon_after', self.initial_attrs.pop('addon_after', ''))

        # These are set in Django or in the global BOOTSTRAP3 settings, and
        # they can be overwritten in the template
        error_css_class = kwargs.get('error_css_class', '')
        required_css_class = kwargs.get('required_css_class', '')
        bound_css_class = kwargs.get('bound_css_class', '')
        if error_css_class:
            self.error_css_class = error_css_class
        else:
            self.error_css_class = getattr(
                field.form, 'error_css_class',
                get_materialize_setting('error_css_class'))
        if required_css_class:
            self.required_css_class = required_css_class
        else:
            self.required_css_class = getattr(
                field.form, 'required_css_class',
                get_materialize_setting('required_css_class'))
        if bound_css_class:
            self.success_css_class = bound_css_class
        else:
            self.success_css_class = getattr(
                field.form, 'bound_css_class',
                get_materialize_setting('success_css_class'))

        # Handle form.empty_permitted
        if self.field.form.empty_permitted:
            self.set_required = False
            self.required_css_class = ''

        self.set_disabled = kwargs.get('set_disabled', False)

    def restore_widget_attrs(self):
        self.widget.attrs = self.initial_attrs

    def add_class_attrs(self):
        classes = self.widget.attrs.get('class', 'validate')
        if self.field_errors:
            classes = add_css_class(classes, 'invalid')
        elif self.field.value():
            classes = add_css_class(classes, 'valid')

        if isinstance(self.widget, Textarea):
            classes = add_css_class(
                classes, 'materialize-textarea', prepend=True)
        elif isinstance(self.widget, ReadOnlyPasswordHashWidget):
            classes = add_css_class(
                classes, 'form-control-static', prepend=True)
        elif not isinstance(self.widget, (CheckboxInput,
                                          RadioSelect,
                                          CheckboxSelectMultiple,
                                          FileInput)):
            classes = add_css_class(classes, 'form-control', prepend=True)
            # For these widget types, add the size class here
            classes = add_css_class(classes, self.get_size_class())
        self.widget.attrs['class'] = classes

    def add_placeholder_attrs(self):
        placeholder = self.widget.attrs.get('placeholder', self.placeholder)
        if placeholder and is_widget_with_placeholder(self.widget):
            self.widget.attrs['placeholder'] = placeholder

    def add_help_attrs(self):
        if not isinstance(self.widget, CheckboxInput):
            self.widget.attrs['title'] = self.widget.attrs.get(
                'title', strip_tags(self.field_help))

    def add_required_attrs(self):
        if self.set_required and is_widget_required_attribute(self.widget):
            self.widget.attrs['required'] = 'required'

    def add_disabled_attrs(self):
        if self.set_disabled:
            self.widget.attrs['disabled'] = 'disabled'

    def add_widget_attrs(self):
        self.add_class_attrs()
        self.add_placeholder_attrs()
        self.add_help_attrs()
        self.add_required_attrs()
        self.add_disabled_attrs()

    def list_to_class(self, html, klass):
        classes = add_css_class(klass, self.get_size_class())
        self.label_class = "outside-label"
        bs = BeautifulSoup(html)
        for tag in bs.ul.find_all('li'):
            tag = tag.extract()
            tag.insert(0, tag.label.input)
            tag.name = 'p'
            bs.ul.append(tag)

        bs.ul.name = 'div'
        return str(bs)

    def put_inside_label(self, html):
        content = '{field} {label}'.format(field=html, label=self.field.label)
        return render_label(
            content=content, label_for=self.field.id_for_label,
            label_title=strip_tags(self.field_help))

    def put_outside_label(self, html):
        content = self.field.label
        self.label_class = "outside-label"
        return html + render_label(
            content=content, label_for=self.field.id_for_label,
            label_title=strip_tags(self.field_help))

    def switch_input(self, html):
        bs = BeautifulSoup(html)
        tmp = '<div class="switch"><label>' + bs.input.attrs.get('off') \
              + html + '<span class="lever"></span>' + bs.input.attrs.get('on') + '</label></div>'
        return tmp

    def range_input(self, html):
        bs = BeautifulSoup(html)
        self.label_class = 'range-label'
        tmp = '<p class="range-field">' + html + '</p>'
        return tmp

    def clearable_file_input(self, html):
        self.form_group_class = 'file-field ' + self.form_group_class
        bs = BeautifulSoup(html)
        [a.attrs.update({'target': '_blank'}) for a in bs.findAll('a')]
        return '<input class="file-path validate" type="text"/><div class="btn"><span>File</span>{input}</div><div class="clearable">{html}</div>'.format(
            input=bs.find('input', {'type': 'file'}).extract(), html=bs)

    def post_widget_render(self, html):
        bs = BeautifulSoup(html)
        if isinstance(self.widget, RadioSelect):
            html = self.list_to_class(html, 'radio')
        elif isinstance(self.widget, CheckboxSelectMultiple):
            html = self.list_to_class(html, 'checkbox')
        elif isinstance(self.widget, SelectDateWidget):
            html = self.fix_date_select_input(html)
        elif isinstance(self.widget, ClearableFileInput):
            html = self.clearable_file_input(html)
        elif isinstance(self.widget, NumberInput):
            if bs.input.attrs.get('type') == 'range':
                html = self.range_input(html)
        elif isinstance(self.widget, CheckboxInput):
            if bs.input.attrs.get('switch'):
                html = self.switch_input(html)
            else:
                html = self.put_outside_label(html)
        return html

    def wrap_widget(self, html):
        if isinstance(self.widget, CheckboxInput):
            checkbox_class = add_css_class('checkbox', self.get_size_class())
            html = \
                '<div class="{klass}">{content}</div>'.format(
                    klass=checkbox_class, content=html
                )
        elif isinstance(self.widget, DateInput):
            bs = BeautifulSoup(html)
            bs.input['class'].append('datepicker')
            html = str(bs)
        return html

    def make_input_group(self, html):
        if (
                    (self.addon_before or self.addon_after) and
                    isinstance(self.widget, (TextInput, DateInput, Select, SelectAddNew))
        ):
            before = '<span class="input-group-addon">{addon}</span>'.format(
                addon=self.addon_before) if self.addon_before else ''
            after = '<span class="input-group-addon">{addon}</span>'.format(
                addon=self.addon_after) if self.addon_after else ''
            html = \
                '<div class="input-group">' + \
                '{before}{html}{after}</div>'.format(
                    before=before,
                    after=after,
                    html=html
                )
        return html

    def append_to_field(self, html):
        help_text_and_errors = [self.field_help] + self.field_errors \
            if self.field_help else self.field_errors
        if help_text_and_errors:
            help_html = get_template(
                'material_field_help_text_and_errors.html'
            ).render(Context({
                'field': self.field,
                'help_text_and_errors': help_text_and_errors,
                'layout': self.layout,
            }))
            html += '<small class="help-block">{help}</small>'.format(
                help=help_html)
        return html

    def get_field_class(self):
        field_class = self.field_class
        if not field_class and self.layout == 'horizontal':
            field_class = self.horizontal_field_class
        return field_class

    def wrap_field(self, html):
        field_class = self.get_field_class()
        if field_class:
            html = '<div class="{klass}">{html}</div>'.format(
                klass=field_class, html=html)
        return html

    def get_label_class(self):
        label_class = self.label_class
        if not label_class and self.layout == 'horizontal':
            label_class = self.horizontal_label_class
        label_class = text_value(label_class)
        if not self.show_label:
            label_class = add_css_class(label_class, 'sr-only')
        return add_css_class(label_class, 'control-label')

    def get_label(self):
        if isinstance(self.widget, CheckboxInput):
            label = None
        else:
            label = self.field.label
        if self.layout == 'horizontal' and not label:
            return '&#160;'
        return label

    def add_label(self, html):
        if isinstance(self.widget, ClearableFileInput):
            return html

        label = self.get_label()
        if label:
            icon = ''
            if self.widget.attrs.get('icon'):
                icon = render_icon(self.widget.attrs.get('icon'), classes='prefix')
            lbl = icon + render_label(
                label,
                label_for=self.field.id_for_label,
                label_class=self.get_label_class())
            if not type(self.widget) in [Select, SelectAddNew]:
                html = lbl + html
            else:
                html += lbl
                bs = BeautifulSoup(html)
                if (type(self.widget) == SelectAddNew) and bs.a:
                    bs.append(bs.a)
                    html = bs

        return html

    def get_form_group_class(self):
        form_group_class = self.form_group_class
        if self.field.field.required and self.required_css_class:
            form_group_class = add_css_class(
                form_group_class, self.required_css_class)

        if self.field.errors and self.error_css_class:
            form_group_class = add_css_class(
                form_group_class, self.error_css_class)
        elif self.field.form.is_bound:
            form_group_class = add_css_class(
                form_group_class, self.success_css_class)
        if self.layout == 'horizontal':
            form_group_class = add_css_class(
                form_group_class, self.get_size_class(prefix='form-group'))
        return form_group_class

    def wrap_label_and_field(self, html):
        return render_form_group(html, self.get_form_group_class())

    def render(self):
        # See if we're not excluded
        if self.field.name in self.exclude.replace(' ', '').split(','):
            return ''
        # Hidden input requires no special treatment
        if self.field.is_hidden:
            return text_value(self.field)
        # Render the widget
        self.add_widget_attrs()
        html = self.field.as_widget(attrs=self.widget.attrs)
        self.restore_widget_attrs()
        # Start post render
        html = self.post_widget_render(html)
        html = self.wrap_widget(html)
        html = self.make_input_group(html)
        html = self.append_to_field(html)
        html = self.wrap_field(html)
        html = self.add_label(html)
        html = self.wrap_label_and_field(html)
        return html


class InlineFieldRenderer(FieldRenderer):
    """
    Inline field renderer
    """

    def add_error_attrs(self):
        field_title = self.widget.attrs.get('title', '')
        field_title += ' ' + ' '.join(
            [strip_tags(e) for e in self.field_errors])
        self.widget.attrs['title'] = field_title.strip()

    def add_widget_attrs(self):
        super(InlineFieldRenderer, self).add_widget_attrs()
        self.add_error_attrs()

    def append_to_field(self, html):
        return html

    def get_field_class(self):
        return self.field_class

    def get_label_class(self):
        return add_css_class(self.label_class, 'sr-only')


class TodoFieldRenderer(FieldRenderer):
    def get_form_group_class(self):
        return self.form_group_class + ' hide'

    def wrap_label_and_field(self, html):
        html = super(TodoFieldRenderer, self).wrap_label_and_field(html)

        return '{pre}{activator}{html}{post}'.format(
            html=html,
            activator=render_todo_item_activator('{}_todo'.format(self.field.id_for_label), self.get_label()),
            pre=render_todo_item_begin() if not self.in_group else '',
            post=render_todo_item_end() if not self.in_group else '')
