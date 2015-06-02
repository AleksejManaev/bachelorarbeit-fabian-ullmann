# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):
    dependencies = [
        ('mentoring', '0010_auto_20150601_1229'),
    ]

    operations = [
        migrations.AlterField(
            model_name='registration',
            name='subject',
            field=models.TextField(default=b'', max_length=250, verbose_name='subject'),
        ),
    ]
