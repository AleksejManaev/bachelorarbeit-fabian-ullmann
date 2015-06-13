# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):
    dependencies = [
        ('mentoring', '0004_auto_20150612_1143'),
    ]

    operations = [
        migrations.AlterField(
            model_name='colloquium',
            name='date_colloquium',
            field=models.DateTimeField(null=True, verbose_name='date colloquium', blank=True),
        ),
    ]
