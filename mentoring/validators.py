from django.conf import settings
from django.core.exceptions import ValidationError


def validate_size(value):
    if not value.file.size <= getattr(settings, 'FILE_UPLOAD_MAX_SIZE'):
        raise ValidationError("This filesize is to big.")
