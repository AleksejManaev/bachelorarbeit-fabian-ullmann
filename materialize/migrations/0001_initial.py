# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='MaterializeForeignModel',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=255)),
                ('subtitle', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='MaterializeTestModel',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('text', models.CharField(max_length=255)),
                ('date', models.DateField(null=True, blank=True)),
                ('message', models.TextField(max_length=1000)),
                ('email', models.EmailField(max_length=254)),
                ('password', models.CharField(max_length=50)),
                ('file', models.FileField(null=True, upload_to=b'', blank=True)),
                ('foreign', models.ForeignKey(blank=True, to='materialize.MaterializeForeignModel', null=True)),
            ],
        ),
    ]
