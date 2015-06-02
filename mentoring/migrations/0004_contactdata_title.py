# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):
    dependencies = [
        ('mentoring', '0003_auto_20150601_0711'),
    ]

    operations = [
        migrations.AddField(
            model_name='contactdata',
            name='title',
            field=models.CharField(max_length=30, null=True, verbose_name='title', blank=True),
        ),
    ]
