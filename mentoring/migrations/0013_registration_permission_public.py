# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):
    dependencies = [
        ('mentoring', '0012_registration_permission_library_tutor'),
    ]

    operations = [
        migrations.AddField(
            model_name='registration',
            name='permission_public',
            field=models.BooleanField(default=False, verbose_name='permission public'),
        ),
    ]
