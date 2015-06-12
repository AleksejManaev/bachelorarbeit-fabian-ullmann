# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):
    dependencies = [
        ('mentoring', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='registration',
            name='pdf_file',
            field=models.FileField(default=None, upload_to=b'', null=True, verbose_name='PDF File'),
        ),
    ]
