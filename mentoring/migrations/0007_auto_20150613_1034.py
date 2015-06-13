# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):
    dependencies = [
        ('mentoring', '0006_auto_20150613_0841'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mentoringreportitem',
            name='report',
            field=models.ForeignKey(to='mentoring.MentoringReport'),
        ),
    ]
