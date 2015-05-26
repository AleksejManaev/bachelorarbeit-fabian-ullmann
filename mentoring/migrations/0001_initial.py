# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings

import mentoring.helpers
import mentoring.validators


class Migration(migrations.Migration):
    dependencies = [
        ('auth', '0006_require_contenttypes_0002'),
    ]

    operations = [
        migrations.CreateModel(
            name='AbstractWork',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_on', models.DateTimeField(auto_now_add=True, verbose_name='date joined', auto_created=True)),
                ('description', models.TextField(null=True, verbose_name='description', blank=True)),
                ('updated_on', models.DateTimeField(auto_now=True, verbose_name='date joined', null=True)),
                ('finished', models.BooleanField(default=False, verbose_name='finished')),
            ],
        ),
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('street', models.CharField(max_length=255, verbose_name='street')),
                ('city', models.CharField(max_length=255, verbose_name='city')),
                ('zip_code', models.CharField(max_length=30, verbose_name='zip code')),
                ('location', models.CharField(max_length=100, verbose_name='location')),
                ('phone', models.CharField(max_length=30, null=True, verbose_name='phone', blank=True)),
                ('web_address', models.CharField(max_length=255, null=True, verbose_name='web address', blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Colloquium',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date_colloquium', models.DateTimeField(verbose_name='date colloquium')),
            ],
        ),
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100, verbose_name='company name')),
            ],
        ),
        migrations.CreateModel(
            name='CompanyRating',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('rate', models.PositiveSmallIntegerField(verbose_name='rate')),
                ('comment', models.TextField(verbose_name='comment')),
                ('public', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='ContactData',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=30, null=True, verbose_name='title', blank=True)),
                ('first_name', models.CharField(max_length=30, verbose_name='first name')),
                ('last_name', models.CharField(max_length=30, verbose_name='last name')),
                ('email', models.EmailField(max_length=254, verbose_name='email')),
                ('phone', models.CharField(max_length=30, verbose_name='phone')),
            ],
        ),
        migrations.CreateModel(
            name='ContactModel',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('first_name', models.CharField(max_length=30, verbose_name='first name')),
                ('last_name', models.CharField(max_length=30, verbose_name='last name')),
            ],
        ),
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('description', models.CharField(max_length=255, verbose_name='description')),
            ],
        ),
        migrations.CreateModel(
            name='Degree',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('description', models.CharField(max_length=255, verbose_name='description')),
            ],
        ),
        migrations.CreateModel(
            name='Mentoring',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date_initial_meeting', models.DateField(null=True, verbose_name='date initial meeting', blank=True)),
                ('date_deadline', models.DateField(null=True, verbose_name='date deadline', blank=True)),
                ('permission_contact', models.BooleanField(default=False, verbose_name='permission contact')),
            ],
        ),
        migrations.CreateModel(
            name='MentoringRequest',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('tutor_email', models.EmailField(max_length=254)),
                ('requested_on', models.DateTimeField(auto_now=True, verbose_name='requested on')),
                ('status', models.CharField(default=b'NR', max_length=2,
                                            choices=[(b'NR', b'not requested'), (b'RE', b'requested'),
                                                     (b'AC', b'accepted'), (b'DE', b'denied')])),
                ('comment', models.TextField(null=True, verbose_name='comment')),
                ('answer', models.TextField(null=True, verbose_name='answer', blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='PortalUser',
            fields=[
                ('user', models.OneToOneField(primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Registration',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateField(verbose_name='date')),
                ('permission_contact', models.BooleanField(default=False, verbose_name='permission contact')),
                ('permission_infocus', models.BooleanField(default=False, verbose_name='permission INFOCUS')),
                ('permission_library', models.BooleanField(default=False, verbose_name='permission library')),
                ('mentoring', models.OneToOneField(to='mentoring.Mentoring')),
            ],
        ),
        migrations.CreateModel(
            name='ResponseExaminationBoard',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('start_editing', models.DateField(verbose_name='start editing')),
                ('stop_editing', models.DateField(verbose_name='stop editing')),
                ('extend_to', models.DateField(verbose_name='extended to')),
                ('delivery', models.DateField(verbose_name='delivery thesis')),
                ('registration', models.OneToOneField(to='mentoring.Registration')),
            ],
        ),
        migrations.CreateModel(
            name='Placement',
            fields=[
                ('abstractwork_ptr',
                 models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False,
                                      to='mentoring.AbstractWork')),
                ('report', models.FileField(blank=True, upload_to=mentoring.helpers.upload_to_report, null=True,
                                            verbose_name='report', validators=[mentoring.validators.validate_pdf,
                                                                               mentoring.validators.validate_size])),
                ('presentation',
                 models.FileField(blank=True, upload_to=mentoring.helpers.upload_to_presentation, null=True,
                                  verbose_name='presentation',
                                  validators=[mentoring.validators.validate_pdf, mentoring.validators.validate_size])),
                ('certificate',
                 models.FileField(blank=True, upload_to=mentoring.helpers.upload_to_certificate, null=True,
                                  verbose_name='certificate',
                                  validators=[mentoring.validators.validate_pdf, mentoring.validators.validate_size])),
            ],
            bases=('mentoring.abstractwork',),
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('portaluser_ptr',
                 models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False,
                                      to='mentoring.PortalUser')),
                ('matriculation_number', models.CharField(max_length=8, verbose_name='matriculation number')),
                ('course', models.ForeignKey(to='mentoring.Course')),
            ],
            bases=('mentoring.portaluser',),
        ),
        migrations.CreateModel(
            name='Thesis',
            fields=[
                ('abstractwork_ptr',
                 models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False,
                                      to='mentoring.AbstractWork')),
                ('student', models.OneToOneField(to='mentoring.Student')),
            ],
            bases=('mentoring.abstractwork',),
        ),
        migrations.CreateModel(
            name='Tutor',
            fields=[
                ('portaluser_ptr',
                 models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False,
                                      to='mentoring.PortalUser')),
            ],
            bases=('mentoring.portaluser',),
        ),
        migrations.CreateModel(
            name='WorkCompany',
            fields=[
                ('work', models.OneToOneField(primary_key=True, serialize=False, to='mentoring.AbstractWork')),
                ('description', models.TextField(null=True, verbose_name='company description', blank=True)),
                ('company', models.ForeignKey(blank=True, to='mentoring.Company', null=True)),
            ],
        ),
        migrations.AddField(
            model_name='mentoring',
            name='tutor_1',
            field=models.OneToOneField(related_name='tutor_1', to='mentoring.MentoringRequest'),
        ),
        migrations.AddField(
            model_name='mentoring',
            name='tutor_2',
            field=models.OneToOneField(related_name='tutor_2', null=True, blank=True, to='mentoring.MentoringRequest'),
        ),
        migrations.AddField(
            model_name='colloquium',
            name='mentoring',
            field=models.OneToOneField(to='mentoring.Mentoring'),
        ),
        migrations.AddField(
            model_name='address',
            name='portal_user',
            field=models.OneToOneField(to='mentoring.PortalUser'),
        ),
        migrations.AddField(
            model_name='placement',
            name='student',
            field=models.OneToOneField(to='mentoring.Student'),
        ),
        migrations.AddField(
            model_name='mentoring',
            name='thesis',
            field=models.OneToOneField(to='mentoring.Thesis'),
        ),
        migrations.AddField(
            model_name='contactdata',
            name='work_company',
            field=models.OneToOneField(to='mentoring.WorkCompany'),
        ),
        migrations.AddField(
            model_name='companyrating',
            name='thesis',
            field=models.ForeignKey(to='mentoring.Thesis'),
        ),
    ]
