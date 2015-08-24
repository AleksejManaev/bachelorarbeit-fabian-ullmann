# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import mentoring.helpers
import django.contrib.auth.models
import django.utils.timezone
from django.conf import settings
import django.core.validators
import mentoring.validators


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0006_require_contenttypes_0002'),
    ]

    operations = [
        migrations.CreateModel(
            name='MentoringUser',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(null=True, verbose_name='last login', blank=True)),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, max_length=30, validators=[django.core.validators.RegexValidator('^[\\w.@+-]+$', 'Enter a valid username. This value may contain only letters, numbers and @/./+/-/_ characters.', 'invalid')], help_text='Required. 30 characters or fewer. Letters, digits and @/./+/-/_ only.', unique=True, verbose_name='username')),
                ('first_name', models.CharField(max_length=30, verbose_name='first name', blank=True)),
                ('last_name', models.CharField(max_length=30, verbose_name='last name', blank=True)),
                ('email', models.EmailField(max_length=254, verbose_name='email address', blank=True)),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('gidNumber', models.IntegerField(null=True)),
            ],
            options={
                'abstract': False,
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='AbstractWork',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_on', models.DateTimeField(auto_now_add=True, verbose_name='date joined', auto_created=True)),
                ('description', models.TextField(null=True, verbose_name='description', blank=True)),
                ('updated_on', models.DateTimeField(auto_now=True, verbose_name='date updated', null=True)),
                ('sent_on', models.DateTimeField(null=True, verbose_name='date sent', blank=True)),
                ('state', models.CharField(default=b'NR', max_length=2, choices=[(b'NR', b'not requested'), (b'RE', b'requested'), (b'AC', b'accepted'), (b'DE', b'denied'), (b'CD', b'canceled')])),
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
                ('description', models.CharField(max_length=50, verbose_name='description')),
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
            name='Event',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateField(null=True, verbose_name='date', blank=True)),
                ('time', models.TimeField(null=True, verbose_name='time', blank=True)),
                ('room', models.CharField(max_length=100, null=True, verbose_name='room', blank=True)),
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
                ('report', models.ForeignKey(to='mentoring.MentoringReport')),
            ],
        ),
        migrations.CreateModel(
            name='MentoringRequest',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('tutor_email', models.EmailField(max_length=254, null=True, verbose_name='Tutor email', blank=True)),
                ('requested_on', models.DateTimeField(verbose_name='requested on', null=True, editable=False)),
                ('state', models.CharField(default=b'NR', max_length=2, choices=[(b'NR', b'not requested'), (b'RE', b'requested'), (b'AC', b'accepted'), (b'DE', b'denied'), (b'CD', b'canceled')])),
                ('comment', models.TextField(null=True, verbose_name='comment', blank=True)),
                ('answer', models.TextField(null=True, verbose_name='answer', blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='PlacementEventRegistration',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('confirmed', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Registration',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('subject', models.TextField(default=b'', max_length=250, verbose_name='subject')),
                ('date', models.DateField(auto_now=True, verbose_name='date', null=True)),
                ('permission_contact', models.BooleanField(default=False, verbose_name='permission contact')),
                ('permission_infocus', models.BooleanField(default=False, verbose_name='permission INFOCUS')),
                ('permission_public', models.BooleanField(default=False, verbose_name='permission public')),
                ('permission_library', models.BooleanField(default=False, verbose_name='permission library')),
                ('permission_library_tutor', models.BooleanField(default=False, verbose_name='permission library tutor')),
                ('pdf_file', models.TextField(null=True, verbose_name='PDF File', blank=True)),
                ('finished', models.BooleanField(default=False)),
                ('mentoring', models.OneToOneField(to='mentoring.Mentoring')),
            ],
        ),
        migrations.CreateModel(
            name='ResponseExaminationBoard',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('start_editing', models.DateField(null=True, verbose_name='start editing', blank=True)),
                ('stop_editing', models.DateField(null=True, verbose_name='stop editing', blank=True)),
                ('extend_to', models.DateField(null=True, verbose_name='extended to', blank=True)),
                ('finished', models.BooleanField(default=False)),
                ('registration', models.OneToOneField(to='mentoring.Registration')),
            ],
        ),
        migrations.CreateModel(
            name='StudentActivePlacement',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
        ),
        migrations.CreateModel(
            name='StudentActiveThesis',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
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
            name='Colloquium',
            fields=[
                ('event_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='mentoring.Event')),
            ],
            bases=('mentoring.event',),
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
                ('report', models.FileField(blank=True, upload_to=mentoring.helpers.upload_to_placement_report, null=True, verbose_name='report placement', validators=[mentoring.validators.validate_pdf, mentoring.validators.validate_size])),
                ('presentation', models.FileField(blank=True, upload_to=mentoring.helpers.upload_to_placement_presentation, null=True, verbose_name='presentation placement', validators=[mentoring.validators.validate_pdf, mentoring.validators.validate_size])),
                ('certificate', models.FileField(blank=True, upload_to=mentoring.helpers.upload_to_placement_certificate, null=True, verbose_name='certificate placement', validators=[mentoring.validators.validate_pdf, mentoring.validators.validate_size])),
                ('public', models.BooleanField(default=False, verbose_name='public placement')),
                ('course', models.ForeignKey(verbose_name='course placement', blank=True, to='mentoring.Course', null=True)),
            ],
            bases=('mentoring.abstractwork',),
        ),
        migrations.CreateModel(
            name='PlacementEvent',
            fields=[
                ('event_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='mentoring.Event')),
                ('course', models.ForeignKey(to='mentoring.Course')),
            ],
            bases=('mentoring.event',),
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
                ('report', models.FileField(blank=True, upload_to=mentoring.helpers.upload_to_thesis_report, null=True, verbose_name='report thesis', validators=[mentoring.validators.validate_pdf, mentoring.validators.validate_size])),
                ('poster', models.FileField(blank=True, upload_to=mentoring.helpers.upload_to_thesis_poster, null=True, verbose_name='poster thesis', validators=[mentoring.validators.validate_pdf, mentoring.validators.validate_size])),
                ('documents_finished', models.BooleanField(default=False)),
                ('course', models.ForeignKey(blank=True, to='mentoring.Course', null=True)),
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
            model_name='mentoringuser',
            name='groups',
            field=models.ManyToManyField(related_query_name='user', related_name='user_set', to='auth.Group', blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', verbose_name='groups'),
        ),
        migrations.AddField(
            model_name='mentoringuser',
            name='user_permissions',
            field=models.ManyToManyField(related_query_name='user', related_name='user_set', to='auth.Permission', blank=True, help_text='Specific permissions for this user.', verbose_name='user permissions'),
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
                ('matriculation_number', models.CharField(max_length=8, null=True, verbose_name='matriculation number', blank=True)),
                ('extern_email', models.EmailField(max_length=254, null=True, blank=True)),
            ],
            bases=('mentoring.portaluser',),
        ),
        migrations.CreateModel(
            name='Tutor',
            fields=[
                ('portaluser_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='mentoring.PortalUser')),
                ('placement_courses', models.ManyToManyField(to='mentoring.Course', null=True, blank=True)),
            ],
            bases=('mentoring.portaluser',),
        ),
        migrations.AddField(
            model_name='tutor2contactdata',
            name='contact',
            field=models.ForeignKey(blank=True, to='mentoring.ContactData', null=True),
        ),
        migrations.AddField(
            model_name='studentactivethesis',
            name='thesis',
            field=models.OneToOneField(null=True, to='mentoring.Thesis'),
        ),
        migrations.AddField(
            model_name='studentactiveplacement',
            name='placement',
            field=models.OneToOneField(null=True, to='mentoring.Placement'),
        ),
        migrations.AddField(
            model_name='placementeventregistration',
            name='event',
            field=models.ForeignKey(to='mentoring.PlacementEvent', null=True),
        ),
        migrations.AddField(
            model_name='placementeventregistration',
            name='placement',
            field=models.OneToOneField(to='mentoring.Placement'),
        ),
        migrations.AddField(
            model_name='mentoringrequest',
            name='thesis',
            field=models.OneToOneField(to='mentoring.Thesis'),
        ),
        migrations.AddField(
            model_name='mentoring',
            name='thesis',
            field=models.OneToOneField(to='mentoring.Thesis'),
        ),
        migrations.AddField(
            model_name='companyrating',
            name='thesis',
            field=models.ForeignKey(to='mentoring.Thesis'),
        ),
        migrations.AddField(
            model_name='colloquium',
            name='mentoring',
            field=models.OneToOneField(to='mentoring.Mentoring'),
        ),
        migrations.AddField(
            model_name='thesis',
            name='student',
            field=models.ForeignKey(to='mentoring.Student'),
        ),
        migrations.AddField(
            model_name='studentactivethesis',
            name='student',
            field=models.OneToOneField(to='mentoring.Student'),
        ),
        migrations.AddField(
            model_name='studentactiveplacement',
            name='student',
            field=models.OneToOneField(to='mentoring.Student'),
        ),
        migrations.AddField(
            model_name='placementevent',
            name='tutor',
            field=models.ForeignKey(to='mentoring.Tutor'),
        ),
        migrations.AddField(
            model_name='placement',
            name='student',
            field=models.ForeignKey(to='mentoring.Student'),
        ),
        migrations.AddField(
            model_name='mentoring',
            name='tutor_1',
            field=models.ForeignKey(to='mentoring.Tutor'),
        ),
        migrations.AddField(
            model_name='address',
            name='student',
            field=models.OneToOneField(to='mentoring.Student'),
        ),
    ]
