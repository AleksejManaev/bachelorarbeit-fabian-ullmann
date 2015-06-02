# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):
    dependencies = [
        ('mentoring', '0004_contactdata_title'),
    ]

    operations = [
        migrations.CreateModel(
            name='TutorContactData',
            fields=[
                ('contactdata_ptr',
                 models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False,
                                      to='mentoring.ContactData')),
                ('tutor', models.OneToOneField(to='mentoring.Tutor')),
            ],
            bases=('mentoring.contactdata',),
        ),
        migrations.DeleteModel(
            name='ContactModel',
        ),
    ]
