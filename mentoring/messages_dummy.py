from django.utils.translation import ugettext

"""
Der Tag "sort_th" in "template_tags.py" verwendet ugettext(), um erst zur Laufzeit bekannte Texte zu übersetzen.
Die Texte können nicht in "django.po" gespeichert werden, ohne dass "makemessages" diese auskommentiert.
Die Texte werden in dieser Methode aufgeführt, damit makemessages diese in "django.po" aufnimmt.
"""
def makemessages_dummy():
    ugettext('State')
