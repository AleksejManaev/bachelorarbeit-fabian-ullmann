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
                ('updated_on', models.DateTimeField(auto_now=True, verbose_name='date updated', null=True)),
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
                ('name', models.CharField(unique=True, max_length=100, verbose_name='company name')),
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
            name='ContactModel',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=30, null=True, verbose_name='title', blank=True)),
                ('phone', models.CharField(max_length=30, null=True, verbose_name='phone', blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('editing_time', models.CharField(default=b'3', max_length=1, verbose_name='editing time thesis', choices=[(b'3', '3 months'), (b'6', '6 months'), (b'8', '8 weeks')])),
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
                ('created_on', models.DateTimeField(auto_now_add=True, auto_created=True)),
            ],
        ),
        migrations.CreateModel(
            name='MentoringReport',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date_initial_meeting', models.DateField(null=True, verbose_name='date initial meeting', blank=True)),
                ('date_deadline', models.DateField(null=True, verbose_name='date deadline', blank=True)),
                ('mentoring', models.OneToOneField(to='mentoring.Mentoring')),
            ],
        ),
        migrations.CreateModel(
            name='MentoringReportItem',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_on', models.DateTimeField(auto_now_add=True, auto_created=True)),
                ('subject', models.CharField(max_length=100, verbose_name='subject')),
                ('message', models.TextField(null=True, verbose_name='message', blank=True)),
                ('report', models.OneToOneField(to='mentoring.MentoringReport')),
            ],
        ),
        migrations.CreateModel(
            name='MentoringRequest',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('tutor_email', models.EmailField(max_length=254, null=True, verbose_name='Tutor email', blank=True)),
                ('requested_on', models.DateTimeField(verbose_name='requested on', null=True, editable=False)),
                ('status', models.CharField(default=b'NR', max_length=2, choices=[(b'NR', b'not requested'), (b'RE', b'requested'), (b'AC', b'accepted'), (b'DE', b'denied')])),
                ('comment', models.TextField(null=True, verbose_name='comment', blank=True)),
                ('answer', models.TextField(null=True, verbose_name='answer', blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Registration',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('subject', models.TextField(default=b'', max_length=250, verbose_name='subject')),
                ('date', models.DateField(auto_now=True, verbose_name='date')),
                ('permission_contact', models.BooleanField(default=False, verbose_name='permission contact')),
                ('permission_infocus', models.BooleanField(default=False, verbose_name='permission INFOCUS')),
                ('permission_public', models.BooleanField(default=False, verbose_name='permission public')),
                ('permission_library', models.BooleanField(default=False, verbose_name='permission library')),
                ('permission_library_tutor', models.BooleanField(default=False, verbose_name='permission library tutor')),
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
            name='Tutor2ContactData',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('mentoring', models.OneToOneField(to='mentoring.Mentoring')),
            ],
        ),
        migrations.CreateModel(
            name='ContactData',
            fields=[
                ('contactmodel_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='mentoring.ContactModel')),
                ('first_name', models.CharField(max_length=30, verbose_name='first name')),
                ('last_name', models.CharField(max_length=30, verbose_name='last name')),
                ('email', models.EmailField(max_length=254, verbose_name='email')),
            ],
            bases=('mentoring.contactmodel',),
        ),
        migrations.CreateModel(
            name='Placement',
            fields=[
                ('abstractwork_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='mentoring.AbstractWork')),
                ('report',
                 models.FileField(blank=True, upload_to=mentoring.helpers.upload_to_placement_report, null=True,
                                  verbose_name='report',
                                  validators=[mentoring.validators.validate_pdf, mentoring.validators.validate_size])),
                ('presentation',
                 models.FileField(blank=True, upload_to=mentoring.helpers.upload_to_placement_presentation, null=True,
                                  verbose_name='presentation',
                                  validators=[mentoring.validators.validate_pdf, mentoring.validators.validate_size])),
                ('certificate',
                 models.FileField(blank=True, upload_to=mentoring.helpers.upload_to_placement_certificate, null=True,
                                  verbose_name='certificate',
                                  validators=[mentoring.validators.validate_pdf, mentoring.validators.validate_size])),
                ('public', models.BooleanField(default=False, verbose_name='public')),
            ],
            bases=('mentoring.abstractwork',),
        ),
        migrations.CreateModel(
            name='PortalUser',
            fields=[
                ('contactmodel_ptr', models.OneToOneField(parent_link=True, auto_created=True, to='mentoring.ContactModel')),
                ('user', models.OneToOneField(primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
            ],
            bases=('mentoring.contactmodel',),
        ),
        migrations.CreateModel(
            name='Thesis',
            fields=[
                ('abstractwork_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='mentoring.AbstractWork')),
            ],
            bases=('mentoring.abstractwork',),
        ),
        migrations.CreateModel(
            name='WorkCompany',
            fields=[
                ('work', models.OneToOneField(primary_key=True, serialize=False, to='mentoring.AbstractWork')),
                ('description', models.TextField(verbose_name='company description')),
                ('company', models.ForeignKey(blank=True, to='mentoring.Company', null=True)),
            ],
        ),
        migrations.AddField(
            model_name='mentoring',
            name='request',
            field=models.OneToOneField(to='mentoring.MentoringRequest'),
        ),
        migrations.AddField(
            model_name='colloquium',
            name='mentoring',
            field=models.OneToOneField(to='mentoring.Mentoring'),
        ),
        migrations.CreateModel(
            name='CompanyContactData',
            fields=[
                ('contactdata_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='mentoring.ContactData')),
                ('work_company', models.OneToOneField(to='mentoring.WorkCompany')),
            ],
            bases=('mentoring.contactdata',),
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('portaluser_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='mentoring.PortalUser')),
                ('matriculation_number', models.CharField(max_length=8, verbose_name='matriculation number')),
                ('extern_email', models.EmailField(max_length=254)),
                ('course', models.ForeignKey(to='mentoring.Course')),
            ],
            bases=('mentoring.portaluser',),
        ),
        migrations.CreateModel(
            name='Tutor',
            fields=[
                ('portaluser_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='mentoring.PortalUser')),
            ],
            bases=('mentoring.portaluser',),
        ),
        migrations.AddField(
            model_name='tutor2contactdata',
            name='contact',
            field=models.OneToOneField(to='mentoring.ContactData'),
        ),
        migrations.AddField(
            model_name='mentoringrequest',
            name='thesis',
            field=models.OneToOneField(to='mentoring.Thesis'),
        ),
        migrations.AddField(
            model_name='companyrating',
            name='thesis',
            field=models.ForeignKey(to='mentoring.Thesis'),
        ),
        migrations.AddField(
            model_name='thesis',
            name='student',
            field=models.OneToOneField(to='mentoring.Student'),
        ),
        migrations.AddField(
            model_name='placement',
            name='student',
            field=models.OneToOneField(to='mentoring.Student'),
        ),
        migrations.AddField(
            model_name='mentoring',
            name='tutor_1',
            field=models.ForeignKey(to='mentoring.Tutor'),
        ),
        migrations.AddField(
            model_name='address',
            name='portal_user',
            field=models.OneToOneField(to='mentoring.Student'),
        ),
    ]
