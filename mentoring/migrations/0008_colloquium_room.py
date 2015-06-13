# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):
    dependencies = [
        ('mentoring', '0007_auto_20150613_1034'),
    ]

    operations = [
        migrations.AddField(
            model_name='colloquium',
            name='room',
            field=models.TextField(max_length=100, null=True, verbose_name='room', blank=True),
        ),
    ]
