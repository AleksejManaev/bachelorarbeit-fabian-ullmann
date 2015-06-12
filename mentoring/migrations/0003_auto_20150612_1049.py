# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):
    dependencies = [
        ('mentoring', '0002_registration_pdf_file'),
    ]

    operations = [
        migrations.AlterField(
            model_name='registration',
            name='pdf_file',
            field=models.FileField(upload_to=b'', null=True, verbose_name='PDF File', blank=True),
        ),
        migrations.AlterField(
            model_name='responseexaminationboard',
            name='delivery',
            field=models.DateField(null=True, verbose_name='delivery thesis'),
        ),
        migrations.AlterField(
            model_name='responseexaminationboard',
            name='extend_to',
            field=models.DateField(null=True, verbose_name='extended to'),
        ),
        migrations.AlterField(
            model_name='responseexaminationboard',
            name='start_editing',
            field=models.DateField(null=True, verbose_name='start editing'),
        ),
        migrations.AlterField(
            model_name='responseexaminationboard',
            name='stop_editing',
            field=models.DateField(null=True, verbose_name='stop editing'),
        ),
    ]
