# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import mentoring.helpers
import mentoring.validators
from decimal import Decimal
from django.conf import settings
import django.core.validators
import django.contrib.auth.models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0006_require_contenttypes_0002'),
    ]

    operations = [
        migrations.CreateModel(
            name='MentoringUser',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('password', models.CharField(verbose_name='password', max_length=128)),
                ('last_login', models.DateTimeField(blank=True, verbose_name='last login', null=True)),
                ('is_superuser', models.BooleanField(help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status', default=False)),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, verbose_name='username', validators=[django.core.validators.RegexValidator('^[\\w.@+-]+$', 'Enter a valid username. This value may contain only letters, numbers and @/./+/-/_ characters.', 'invalid')], unique=True, max_length=30, help_text='Required. 30 characters or fewer. Letters, digits and @/./+/-/_ only.')),
                ('first_name', models.CharField(blank=True, verbose_name='first name', max_length=30)),
                ('last_name', models.CharField(blank=True, verbose_name='last name', max_length=30)),
                ('email', models.EmailField(blank=True, verbose_name='email address', max_length=254)),
                ('is_staff', models.BooleanField(help_text='Designates whether the user can log into this admin site.', verbose_name='staff status', default=False)),
                ('is_active', models.BooleanField(help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active', default=True)),
                ('date_joined', models.DateTimeField(verbose_name='date joined', default=django.utils.timezone.now)),
                ('gidNumber', models.IntegerField(null=True)),
            ],
            options={
                'verbose_name_plural': 'users',
                'verbose_name': 'user',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='AbstractWork',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('created_on', models.DateTimeField(auto_now_add=True, verbose_name='date joined', auto_created=True)),
                ('task', models.TextField(verbose_name='task', null=True)),
                ('updated_on', models.DateTimeField(verbose_name='date updated', auto_now=True, null=True)),
                ('sent_on', models.DateTimeField(blank=True, verbose_name='date sent', null=True)),
                ('comment_unread_by_student', models.BooleanField(default=False)),
                ('comment_unread_by_tutor', models.BooleanField(default=False)),
                ('mentoring_requested', models.BooleanField(verbose_name='Requested', default=False)),
                ('mentoring_accepted', models.CharField(choices=[('ND', '-'), ('MA', 'Accepted'), ('MD', 'Denied')], max_length=2, default='ND')),
                ('archived', models.BooleanField(verbose_name='Archived', default=False)),
                ('completed', models.CharField(choices=[('-', '-'), ('Completed', 'Completed'), ('Failed', 'Failed')], verbose_name='Completed', max_length=100, default='-')),
            ],
        ),
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('street', models.CharField(verbose_name='street', max_length=255)),
                ('city', models.CharField(verbose_name='city', max_length=255)),
                ('zip_code', models.CharField(verbose_name='zip code', max_length=30)),
                ('location', models.CharField(verbose_name='location', max_length=100)),
                ('web_address', models.CharField(blank=True, verbose_name='web address', max_length=255, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('message', models.TextField(verbose_name='message')),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('private', models.BooleanField(verbose_name='Only visible for me', default=False)),
            ],
        ),
        migrations.CreateModel(
            name='ContactModel',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('title', models.CharField(blank=True, verbose_name='title', max_length=30, null=True)),
                ('phone', models.CharField(blank=True, verbose_name='phone', max_length=30, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Seminar',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('year', models.IntegerField(blank=True, verbose_name='Year', null=True)),
                ('type', models.CharField(choices=[('placement', 'placement'), ('bachelor', 'bachelor'), ('master', 'master')], verbose_name='Seminar type', max_length=10)),
            ],
            options={
                'verbose_name': 'Seminar',
            },
        ),
        migrations.CreateModel(
            name='SeminarEntry',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('date', models.DateTimeField()),
                ('seminar', models.ForeignKey(to='mentoring.Seminar')),
            ],
        ),
        migrations.CreateModel(
            name='StudentActivePlacement',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='StudentActiveThesis',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='ContactData',
            fields=[
                ('contactmodel_ptr', models.OneToOneField(serialize=False, parent_link=True, primary_key=True, to='mentoring.ContactModel', auto_created=True)),
                ('first_name', models.CharField(blank=True, verbose_name='First name', max_length=30, null=True)),
                ('last_name', models.CharField(blank=True, verbose_name='Last name', max_length=30, null=True)),
                ('email', models.EmailField(blank=True, verbose_name='Email', max_length=254, null=True)),
            ],
            bases=('mentoring.contactmodel',),
        ),
        migrations.CreateModel(
            name='Placement',
            fields=[
                ('abstractwork_ptr', models.OneToOneField(serialize=False, parent_link=True, primary_key=True, to='mentoring.AbstractWork', auto_created=True)),
                ('company_name', models.CharField(blank=True, verbose_name='company name', max_length=100, null=True)),
                ('company_address', models.TextField(blank=True, verbose_name='company address', null=True)),
                ('date_from', models.DateField(blank=True, verbose_name='internship begin', null=True)),
                ('date_to', models.DateField(blank=True, verbose_name='internship end', null=True)),
                ('report', models.FileField(blank=True, verbose_name='Placement report', upload_to=mentoring.helpers.upload_to_placement_report, validators=[mentoring.validators.validate_size], null=True)),
                ('report_uploaded_date', models.DateTimeField(blank=True, null=True)),
                ('certificate', models.FileField(blank=True, verbose_name='Placement certificate', upload_to=mentoring.helpers.upload_to_placement_certificate, validators=[mentoring.validators.validate_size], null=True)),
                ('state', models.CharField(choices=[('Not requested', 'Not requested'), ('Requested', 'Requested'), ('Mentoring denied', 'Mentoring denied'), ('Mentoring accepted', 'Mentoring accepted'), ('Seminar completed', 'Seminar completed'), ('Report accepted', 'Report accepted'), ('Certificate accepted', 'Certificate accepted'), ('Placement completed', 'Placement completed'), ('Placement failed', 'Placement failed'), ('Archived', 'Archived')], verbose_name='State', max_length=100, default='Not requested')),
                ('report_accepted', models.BooleanField(verbose_name='Report accepted', default=False)),
                ('certificate_accepted', models.BooleanField(verbose_name='Certificate accepted', default=False)),
            ],
            bases=('mentoring.abstractwork',),
        ),
        migrations.CreateModel(
            name='PortalUser',
            fields=[
                ('contactmodel_ptr', models.OneToOneField(parent_link=True, to='mentoring.ContactModel', auto_created=True)),
                ('user', models.OneToOneField(serialize=False, to=settings.AUTH_USER_MODEL, primary_key=True)),
            ],
            bases=('mentoring.contactmodel',),
        ),
        migrations.CreateModel(
            name='Thesis',
            fields=[
                ('abstractwork_ptr', models.OneToOneField(serialize=False, parent_link=True, primary_key=True, to='mentoring.AbstractWork', auto_created=True)),
                ('type', models.CharField(choices=[('Bachelor', 'Bachelor'), ('Master', 'Master')], verbose_name='Type', max_length=100, default='Bachelor')),
                ('second_examiner_first_name', models.CharField(blank=True, verbose_name='First name', max_length=30, null=True)),
                ('second_examiner_last_name', models.CharField(blank=True, verbose_name='Last name', max_length=30, null=True)),
                ('second_examiner_organisation', models.CharField(blank=True, verbose_name='Organisation', max_length=30, null=True)),
                ('second_examiner_title', models.CharField(blank=True, verbose_name='title', max_length=30, null=True)),
                ('expose', models.FileField(blank=True, verbose_name='Expose', upload_to=mentoring.helpers.upload_to_thesis_expose, validators=[mentoring.validators.validate_size], null=True)),
                ('poster', models.FileField(blank=True, verbose_name='Poster', upload_to=mentoring.helpers.upload_to_thesis_poster, validators=[mentoring.validators.validate_size], null=True)),
                ('thesis', models.FileField(blank=True, verbose_name='Thesis', upload_to=mentoring.helpers.upload_to_thesis_thesis, validators=[mentoring.validators.validate_size], null=True)),
                ('presentation', models.FileField(blank=True, verbose_name='Presentation', upload_to=mentoring.helpers.upload_to_thesis_presentation, null=True)),
                ('other', models.FileField(blank=True, verbose_name='Other', upload_to=mentoring.helpers.upload_to_thesis_other, null=True)),
                ('grade_first_examiner', models.DecimalField(blank=True, verbose_name='Grade first examiner', max_digits=2, choices=[(Decimal('1.0'), '1,0'), (Decimal('1.3'), '1,3'), (Decimal('1.7'), '1,7'), (Decimal('2.0'), '2,0'), (Decimal('2.3'), '2,3'), (Decimal('2.7'), '2,7'), (Decimal('3.0'), '3,0'), (Decimal('3.3'), '3,3'), (Decimal('3.7'), '3,7'), (Decimal('4.0'), '4,0'), (Decimal('5.0'), '5,0')], null=True, decimal_places=1)),
                ('grade_second_examiner', models.DecimalField(blank=True, verbose_name='Grade second examiner', max_digits=2, choices=[(Decimal('1.0'), '1,0'), (Decimal('1.3'), '1,3'), (Decimal('1.7'), '1,7'), (Decimal('2.0'), '2,0'), (Decimal('2.3'), '2,3'), (Decimal('2.7'), '2,7'), (Decimal('3.0'), '3,0'), (Decimal('3.3'), '3,3'), (Decimal('3.7'), '3,7'), (Decimal('4.0'), '4,0'), (Decimal('5.0'), '5,0')], null=True, decimal_places=1)),
                ('grade_presentation', models.DecimalField(blank=True, verbose_name='Grade presentation', max_digits=2, choices=[(Decimal('1.0'), '1,0'), (Decimal('1.3'), '1,3'), (Decimal('1.7'), '1,7'), (Decimal('2.0'), '2,0'), (Decimal('2.3'), '2,3'), (Decimal('2.7'), '2,7'), (Decimal('3.0'), '3,0'), (Decimal('3.3'), '3,3'), (Decimal('3.7'), '3,7'), (Decimal('4.0'), '4,0'), (Decimal('5.0'), '5,0')], null=True, decimal_places=1)),
                ('examination_office_state', models.CharField(choices=[('1A', 'Not submitted'), ('1B', 'Submitted'), ('2A', 'Accepted'), ('2B', 'Denied')], verbose_name='Examination office state', max_length=100, default='1A')),
                ('deadline', models.DateTimeField(blank=True, verbose_name='Deadline', null=True)),
                ('deadline_extended', models.BooleanField(verbose_name='Deadline extended', default=False)),
                ('colloquium_done', models.BooleanField(verbose_name='Colloquium done', default=False)),
                ('poster_printed', models.BooleanField(verbose_name='Poster printed', default=False)),
                ('poster_accepted', models.BooleanField(verbose_name='Poster accepted', default=False)),
                ('state', models.CharField(choices=[('Not requested', 'Not requested'), ('Requested', 'Requested'), ('Mentoring accepted', 'Mentoring accepted'), ('Mentoring denied', 'Mentoring denied'), ('Examination office submitted', 'Examination office submitted'), ('Examination office accepted', 'Examination office accepted'), ('Thesis submitted', 'Thesis submitted'), ('Colloquium completed', 'Colloquium completed'), ('Seminar completed', 'Seminar completed'), ('Poster accepted', 'Poster accepted'), ('Thesis completion', 'Thesis completion'), ('Thesis failed', 'Thesis failed'), ('Archived', 'Archived')], verbose_name='State', max_length=100, default='Not requested')),
            ],
            bases=('mentoring.abstractwork',),
        ),
        migrations.AlterUniqueTogether(
            name='seminar',
            unique_together=set([('year', 'type')]),
        ),
        migrations.AddField(
            model_name='comment',
            name='abstractwork',
            field=models.ForeignKey(to='mentoring.AbstractWork'),
        ),
        migrations.AddField(
            model_name='comment',
            name='author',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='mentoringuser',
            name='groups',
            field=models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', to='auth.Group', related_name='user_set', verbose_name='groups', related_query_name='user'),
        ),
        migrations.AddField(
            model_name='mentoringuser',
            name='user_permissions',
            field=models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', to='auth.Permission', related_name='user_set', verbose_name='user permissions', related_query_name='user'),
        ),
        migrations.CreateModel(
            name='PlacementCompanyContactData',
            fields=[
                ('contactdata_ptr', models.OneToOneField(serialize=False, parent_link=True, primary_key=True, to='mentoring.ContactData', auto_created=True)),
                ('placement', models.OneToOneField(null=True, to='mentoring.Placement')),
            ],
            bases=('mentoring.contactdata',),
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('portaluser_ptr', models.OneToOneField(serialize=False, parent_link=True, primary_key=True, to='mentoring.PortalUser', auto_created=True)),
                ('matriculation_number', models.CharField(blank=True, verbose_name='Matriculation number', max_length=8, null=True)),
                ('course', models.CharField(choices=[('-', '-'), ('B-INF', 'B-INF'), ('M-INF', 'M-INF'), ('B-OSMI', 'B-OSMI'), ('M-OSMI', 'M-OSMI'), ('B-MEDINF', 'B-MEDINF'), ('B-ACS', 'B-ACS'), ('M-DM', 'M-DM')], verbose_name='Course', max_length=30, default='-')),
                ('extern_email', models.EmailField(blank=True, verbose_name='extern email address', max_length=254, null=True)),
                ('placement_year', models.IntegerField(blank=True, verbose_name='Placement year', null=True)),
                ('bachelor_year', models.IntegerField(blank=True, verbose_name='Bachelor year', null=True)),
                ('master_year', models.IntegerField(blank=True, verbose_name='Master year', null=True)),
                ('placement_seminar_done', models.BooleanField(verbose_name='Placement seminar done', default=False)),
                ('bachelor_seminar_done', models.BooleanField(verbose_name='Bachelor seminar done', default=False)),
                ('master_seminar_done', models.BooleanField(verbose_name='Master seminar done', default=False)),
                ('bachelor_seminar_presentation_date', models.ForeignKey(null=True, related_name='bachelor_seminar_presentation_student', to='mentoring.SeminarEntry', blank=True)),
                ('master_seminar_presentation_date', models.ForeignKey(null=True, related_name='master_seminar_presentation_student', to='mentoring.SeminarEntry', blank=True)),
                ('placement_seminar_presentation_date', models.ForeignKey(null=True, related_name='placement_seminar_presentation_student', to='mentoring.SeminarEntry', blank=True)),
                ('seminar_entries', models.ManyToManyField(related_name='seminar_students', to='mentoring.SeminarEntry')),
            ],
            bases=('mentoring.portaluser',),
        ),
        migrations.CreateModel(
            name='Tutor',
            fields=[
                ('portaluser_ptr', models.OneToOneField(serialize=False, parent_link=True, primary_key=True, to='mentoring.PortalUser', auto_created=True)),
                ('placement_responsible', models.BooleanField(default=False)),
                ('thesis_responsible', models.BooleanField(default=False)),
                ('poster_responsible', models.BooleanField(default=False)),
            ],
            bases=('mentoring.portaluser',),
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
            model_name='address',
            name='student',
            field=models.OneToOneField(to='mentoring.Student'),
        ),
        migrations.AddField(
            model_name='abstractwork',
            name='student',
            field=models.ForeignKey(to='mentoring.Student', null=True),
        ),
        migrations.AddField(
            model_name='abstractwork',
            name='tutor',
            field=models.ForeignKey(to='mentoring.Tutor', null=True),
        ),
    ]
