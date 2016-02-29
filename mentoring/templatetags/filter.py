from datetime import datetime
import re
from django import template
from django.utils.translation import ugettext_lazy as _

__author__ = 'ullmanfa'
register = template.Library()

numeric_test = re.compile("^\d+$")


@register.filter
def bool2string(value, *args):
    if value:
        return _('Yes')
    else:
        return _('No')


@register.filter
def state_css(value, *args):
    if value == 'ND':
        return 'alert-warning'
    elif value == 'MA':
        return 'alert-success'
    elif value == 'MD':
        return 'alert-danger'
    else:
        return 'alert-info'


@register.filter
def state(value, *args):
    if value == 'ND':
        return _('requested')
    elif value == 'MA':
        return _('mentoring accepted')
    elif value == 'MD':
        return _('mentoring denied')
    else:
        return _('error')


@register.filter
def state_checked(value, *args):
    if value == 'MA' or value == 'IA':
        return 'checked="checked"'
    elif value == 'MD' or value == 'ID':
        return ''


@register.filter
def boolean_checked(value, *args):
    if value is True:
        return 'checked="checked"'
    elif value is False:
        return ''


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
