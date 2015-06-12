# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):
    dependencies = [
        ('mentoring', '0003_auto_20150612_1049'),
    ]

    operations = [
        migrations.AlterField(
            model_name='responseexaminationboard',
            name='delivery',
            field=models.DateField(null=True, verbose_name='delivery thesis', blank=True),
        ),
        migrations.AlterField(
            model_name='responseexaminationboard',
            name='extend_to',
            field=models.DateField(null=True, verbose_name='extended to', blank=True),
        ),
        migrations.AlterField(
            model_name='responseexaminationboard',
            name='start_editing',
            field=models.DateField(null=True, verbose_name='start editing', blank=True),
        ),
        migrations.AlterField(
            model_name='responseexaminationboard',
            name='stop_editing',
            field=models.DateField(null=True, verbose_name='stop editing', blank=True),
        ),
    ]
