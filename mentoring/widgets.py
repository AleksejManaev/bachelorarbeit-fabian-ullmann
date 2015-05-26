from django.forms import ClearableFileInput

__author__ = 'ullmanfa'


class PdfFileInput(ClearableFileInput):
    def __init__(self, attrs):
        super(PdfFileInput, self).__init__()
