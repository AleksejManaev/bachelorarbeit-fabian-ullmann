# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):
    dependencies = [
        ('mentoring', '0005_auto_20150601_0915'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tutorcontactdata',
            name='contactdata_ptr',
        ),
        migrations.RemoveField(
            model_name='tutorcontactdata',
            name='tutor',
        ),
        migrations.AddField(
            model_name='portaluser',
            name='title',
            field=models.CharField(max_length=30, null=True, verbose_name='title', blank=True),
        ),
        migrations.DeleteModel(
            name='TutorContactData',
        ),
    ]
