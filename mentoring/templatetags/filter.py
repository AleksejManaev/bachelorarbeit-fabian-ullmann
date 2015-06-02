import re

from django import template
from django.utils.translation import ugettext_lazy as _

__author__ = 'ullmanfa'
register = template.Library()

numeric_test = re.compile("^\d+$")


@register.filter
def state(value, *args):
    if value == 'NR':
        return _('not requested')
    elif value == 'RE':
        return _('requested')
    elif value == 'AC':
        return _('accepted')
    elif value == 'DE':
        return _('denied')
    else:
        return _('error')


@register.filter
def for_request(value, *args):
    return value in ['NR', 'DE']
