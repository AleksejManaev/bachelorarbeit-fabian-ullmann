import hashlib

from django.db import models

__author__ = 'ullmanfa'
import time


def createHash():
    """This function generate 10 character long hash"""
    hash = hashlib.sha1()
    hash.update(str(time.time()))
    return hash.hexdigest()[:10]


def upload_to_placement_report(instance, filename):
    uri = '%s/placement/report/%s' % (instance.student.matriculation_number, filename)
    return uri


def upload_to_placement_presentation(instance, filename):
    uri = '%s/placement/presentation/%s' % (instance.student.matriculation_number, filename)
    return uri


def upload_to_placement_certificate(instance, filename):
    uri = '%s/placement/certificate/%s' % (instance.student.matriculation_number, filename)
    return uri


def upload_to_thesis_thesis(instance, filename):
    uri = '%s/thesis/documents/thesis/%s' % (instance.student.matriculation_number, filename)
    return uri


def upload_to_thesis_poster(instance, filename):
    uri = '%s/thesis/documents/poster/%s' % (instance.student.matriculation_number, filename)
    return uri

class ContentTypeRestrictedFileField(models.FileField):
    """
    Same as FileField, but you can specify:
        * content_types - list containing allowed content_types. Example: ['application/pdf', 'image/jpeg']
        * max_upload_size - a number indicating the maximum file size allowed for upload.
            2.5MB - 2621440
            5MB - 5242880
            10MB - 10485760
            20MB - 20971520
            50MB - 5242880
            100MB 104857600
            250MB - 214958080
            500MB - 429916160
    """
    pass
