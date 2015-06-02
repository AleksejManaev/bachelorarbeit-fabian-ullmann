# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):
    dependencies = [
        ('mentoring', '0002_auto_20150530_1546'),
    ]

    operations = [
        migrations.AlterField(
            model_name='address',
            name='portal_user',
            field=models.OneToOneField(to='mentoring.Student'),
        ),
    ]
