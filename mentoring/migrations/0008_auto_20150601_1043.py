# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):
    dependencies = [
        ('mentoring', '0007_auto_20150601_0928'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tutor2contactdata',
            name='contactdata_ptr',
        ),
        migrations.AddField(
            model_name='tutor2contactdata',
            name='contact',
            field=models.OneToOneField(default=1, to='mentoring.ContactData'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='tutor2contactdata',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, default=1, serialize=False, verbose_name='ID'),
            preserve_default=False,
        ),
    ]
