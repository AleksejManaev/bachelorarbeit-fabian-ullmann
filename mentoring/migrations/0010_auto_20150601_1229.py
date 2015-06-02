# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):
    dependencies = [
        ('mentoring', '0009_auto_20150601_1136'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='editing_time',
            field=models.CharField(default=b'3', max_length=1, verbose_name='editing time thesis',
                                   choices=[(b'3', '3 months'), (b'6', '6 months'), (b'8', '8 weeks')]),
        ),
        migrations.AlterField(
            model_name='registration',
            name='subject',
            field=models.TextField(default=b'', max_length=1000, verbose_name='subject'),
        ),
    ]
