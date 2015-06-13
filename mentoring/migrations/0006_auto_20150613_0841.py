# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):
    dependencies = [
        ('mentoring', '0005_auto_20150613_0831'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='colloquium',
            name='date_colloquium',
        ),
        migrations.AddField(
            model_name='colloquium',
            name='date',
            field=models.DateField(null=True, verbose_name='date', blank=True),
        ),
        migrations.AddField(
            model_name='colloquium',
            name='time',
            field=models.TimeField(null=True, verbose_name='time', blank=True),
        ),
    ]
