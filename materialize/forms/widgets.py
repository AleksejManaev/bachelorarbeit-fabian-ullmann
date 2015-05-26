from django.forms.utils import flatatt
from django.forms.widgets import Select
from django.utils.html import format_html
from django.utils.safestring import mark_safe

__author__ = 'ullmanfa'


class SelectAddNew(Select):
    def __init__(self, attrs=None, choices=(), create_url=None):
        super(SelectAddNew, self).__init__(attrs, choices)
        self.create_url = create_url

    def render(self, name, value, attrs=None, choices=()):
        if value is None:
            value = ''
        final_attrs = self.build_attrs(attrs, name=name)
        output = [format_html('<select{}>', flatatt(final_attrs))]
        options = self.render_options(choices, [value])
        if options:
            output.append(options)

        if self.create_url:
            output.append('</select><a href="{}">add</a>'.format(self.create_url))
        return mark_safe('\n'.join(output))
