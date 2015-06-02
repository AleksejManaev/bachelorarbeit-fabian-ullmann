# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):
    dependencies = [
        ('mentoring', '0006_auto_20150601_0924'),
    ]

    operations = [
        migrations.CreateModel(
            name='ContactModel',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=30, null=True, verbose_name='title', blank=True)),
                ('phone', models.CharField(max_length=30, null=True, verbose_name='phone', blank=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='address',
            name='phone',
        ),
        migrations.RemoveField(
            model_name='contactdata',
            name='id',
        ),
        migrations.RemoveField(
            model_name='contactdata',
            name='phone',
        ),
        migrations.RemoveField(
            model_name='contactdata',
            name='title',
        ),
        migrations.RemoveField(
            model_name='portaluser',
            name='title',
        ),
        migrations.AddField(
            model_name='contactdata',
            name='contactmodel_ptr',
            field=models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, default=1,
                                       serialize=False, to='mentoring.ContactModel'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='portaluser',
            name='contactmodel_ptr',
            field=models.OneToOneField(parent_link=True, auto_created=True, default=2, to='mentoring.ContactModel'),
            preserve_default=False,
        ),
    ]
