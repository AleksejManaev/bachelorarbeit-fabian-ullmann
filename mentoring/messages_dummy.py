from django.utils.translation import ugettext

"""
An einigen Stellen werden Texte übersetzt, die erst zur Laufzeit bekannt werden. Dies geschieht über den Aufruf der Methode ugettext() oder
von {% trans %}. Die Texte können nicht in "django.po" gespeichert werden, ohne dass diese durch "makemessages" auskommentiert werden.
Deshalb werden die Texte in dieser Methode aufgeführt, damit makemessages diese in "django.po" aufnimmt.
"""


def makemessages_dummy():
    ugettext('State')
    ugettext('Accepted')
    ugettext('Denied')
    ugettext('Sent')
    ugettext('Not decided')
    ugettext('Not sent')

