from datetime import datetime
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
    elif value == 'CD':
        return _('canceled')
    else:
        return _('error')


@register.filter
def for_request(value, *args):
    return value in ['NR', 'DE']


@register.filter
def confirmed(value, arg=None):
    return value.filter(confirmed=True)


@register.filter
def not_confirmed(value, arg=None):
    return value.filter(confirmed=False)


@register.filter
def date_future(value, arg=None):
    return value.filter(date__gte=datetime.now().date())


@register.filter
def date_past(value, arg=None):
    return value.filter(date__lte=datetime.now().date())


@register.filter
def placementeventregistration(value, arg=None):
    l = []
    for i in value:
        t = None
        if arg == None:
            t = i.placementeventregistration_set.all()

        else:
            t = i.placementeventregistration_set.filter(confirmed=arg)
        if len(t) > 0:
            for i in t:
                l.append(i)
    return l
