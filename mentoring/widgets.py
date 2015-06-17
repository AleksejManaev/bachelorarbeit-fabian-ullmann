from django.forms import ClearableFileInput

__author__ = 'ullmanfa'


class PdfFileInput(ClearableFileInput):
    def __init__(self, attrs):
        super(PdfFileInput, self).__init__()


class ClearableFileInput(ClearableFileInput):
    template_with_initial = (
        '%(initial_text)s: <a href="%(initial_url)s">%(initial)s</a> '
        '%(clear_template)s %(input)s'
    )
