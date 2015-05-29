from django.conf import settings
from django.core.exceptions import ValidationError


def validate_pdf(value):
    if not value.read(5) == '%PDF-':
        raise ValidationError("This file is not in PDF format.")

def validate_size(value):
    print(value)
    print(value.file.size)
    if not value.file.size <= getattr(settings, 'FILE_UPLOAD_MAX_SIZE'):
        print "ValidationError size"
        raise ValidationError("This filesize is to big.")
