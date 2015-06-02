# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):
    dependencies = [
        ('mentoring', '0011_auto_20150602_0652'),
    ]

    operations = [
        migrations.AddField(
            model_name='registration',
            name='permission_library_tutor',
            field=models.BooleanField(default=False, verbose_name='permission library tutor'),
        ),
    ]
