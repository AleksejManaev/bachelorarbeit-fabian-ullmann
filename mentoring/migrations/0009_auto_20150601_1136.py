# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):
    dependencies = [
        ('mentoring', '0008_auto_20150601_1043'),
    ]

    operations = [
        migrations.AddField(
            model_name='registration',
            name='subject',
            field=models.TextField(default=b'', max_length=1000, verbose_name='label'),
        ),
        migrations.AlterField(
            model_name='registration',
            name='date',
            field=models.DateField(auto_now=True, verbose_name='date'),
        ),
    ]
