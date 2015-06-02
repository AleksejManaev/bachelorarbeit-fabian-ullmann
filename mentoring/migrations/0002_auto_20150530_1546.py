# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):
    dependencies = [
        ('mentoring', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tutor2ContactData',
            fields=[
                ('contactdata_ptr',
                 models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False,
                                      to='mentoring.ContactData')),
            ],
            bases=('mentoring.contactdata',),
        ),
        migrations.RemoveField(
            model_name='mentoring',
            name='tutor_2',
        ),
        migrations.AddField(
            model_name='tutor2contactdata',
            name='mentoring',
            field=models.OneToOneField(to='mentoring.Mentoring'),
        ),
    ]
