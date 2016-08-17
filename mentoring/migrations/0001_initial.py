# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.contrib.auth.models
from decimal import Decimal
import django.utils.timezone
import mentoring.validators
import django.core.validators
import mentoring.helpers
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0006_require_contenttypes_0002'),
    ]

    operations = [
        migrations.CreateModel(
            name='MentoringUser',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('password', models.CharField(verbose_name='password', max_length=128)),
                ('last_login', models.DateTimeField(verbose_name='last login', blank=True, null=True)),
                ('is_superuser', models.BooleanField(verbose_name='superuser status', default=False, help_text='Designates that this user has all permissions without explicitly assigning them.')),
                ('username', models.CharField(verbose_name='username', max_length=30, validators=[django.core.validators.RegexValidator('^[\\w.@+-]+$', 'Enter a valid username. This value may contain only letters, numbers and @/./+/-/_ characters.', 'invalid')], error_messages={'unique': 'A user with that username already exists.'}, unique=True, help_text='Required. 30 characters or fewer. Letters, digits and @/./+/-/_ only.')),
                ('first_name', models.CharField(verbose_name='first name', blank=True, max_length=30)),
                ('last_name', models.CharField(verbose_name='last name', blank=True, max_length=30)),
                ('email', models.EmailField(verbose_name='email address', blank=True, max_length=254)),
                ('is_staff', models.BooleanField(verbose_name='staff status', default=False, help_text='Designates whether the user can log into this admin site.')),
                ('is_active', models.BooleanField(verbose_name='active', default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.')),
                ('date_joined', models.DateTimeField(verbose_name='date joined', default=django.utils.timezone.now)),
                ('gidNumber', models.IntegerField(null=True)),
            ],
            options={
                'verbose_name': 'user',
                'abstract': False,
                'verbose_name_plural': 'users',
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='AbstractWork',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('created_on', models.DateTimeField(verbose_name='date joined', auto_created=True, auto_now_add=True)),
                ('task', models.TextField(verbose_name='task', null=True)),
                ('updated_on', models.DateTimeField(verbose_name='date updated', null=True, auto_now=True)),
                ('sent_on', models.DateTimeField(verbose_name='date sent', blank=True, null=True)),
                ('comment_unread_by_student', models.BooleanField(default=False)),
                ('comment_unread_by_tutor', models.BooleanField(default=False)),
                ('mentoring_requested', models.BooleanField(verbose_name='Requested', default=False)),
                ('mentoring_accepted', models.CharField(choices=[('ND', '-'), ('MA', 'Accepted'), ('MD', 'Denied')], default='ND', max_length=2)),
                ('archived', models.BooleanField(verbose_name='Archived', default=False)),
                ('completed', models.CharField(verbose_name='Completed', choices=[('-', '-'), ('Completed', 'Completed'), ('Failed', 'Failed')], default='-', max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('street', models.CharField(verbose_name='street', max_length=255)),
                ('city', models.CharField(verbose_name='city', max_length=255)),
                ('zip_code', models.CharField(verbose_name='zip code', max_length=30)),
                ('location', models.CharField(verbose_name='location', max_length=100)),
                ('web_address', models.CharField(verbose_name='web address', blank=True, null=True, max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('message', models.TextField(verbose_name='message')),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('private', models.BooleanField(verbose_name='Only visible for me', default=False)),
            ],
        ),
        migrations.CreateModel(
            name='ContactModel',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('title', models.CharField(verbose_name='title', blank=True, null=True, max_length=30)),
                ('phone', models.CharField(verbose_name='phone', blank=True, null=True, max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='Seminar',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('year', models.IntegerField(verbose_name='Year', blank=True, null=True)),
                ('type', models.CharField(verbose_name='Seminar type', choices=[('placement', 'placement'), ('bachelor', 'bachelor'), ('master', 'master')], max_length=10)),
            ],
            options={
                'verbose_name': 'Seminar',
            },
        ),
        migrations.CreateModel(
            name='SeminarEntry',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('date', models.DateTimeField()),
                ('seminar', models.ForeignKey(to='mentoring.Seminar')),
            ],
        ),
        migrations.CreateModel(
            name='StudentActivePlacement',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
            ],
        ),
        migrations.CreateModel(
            name='StudentActiveThesis',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
            ],
        ),
        migrations.CreateModel(
            name='ContactData',
            fields=[
                ('contactmodel_ptr', models.OneToOneField(primary_key=True, to='mentoring.ContactModel', auto_created=True, serialize=False, parent_link=True)),
                ('first_name', models.CharField(verbose_name='First name', blank=True, null=True, max_length=30)),
                ('last_name', models.CharField(verbose_name='Last name', blank=True, null=True, max_length=30)),
                ('email', models.EmailField(verbose_name='Email', blank=True, null=True, max_length=254)),
            ],
            bases=('mentoring.contactmodel',),
        ),
        migrations.CreateModel(
            name='Placement',
            fields=[
                ('abstractwork_ptr', models.OneToOneField(primary_key=True, to='mentoring.AbstractWork', auto_created=True, serialize=False, parent_link=True)),
                ('company_name', models.CharField(verbose_name='company name', blank=True, null=True, max_length=100)),
                ('company_address', models.TextField(verbose_name='company address', blank=True, null=True)),
                ('date_from', models.DateField(verbose_name='internship begin', blank=True, null=True)),
                ('date_to', models.DateField(verbose_name='internship end', blank=True, null=True)),
                ('report', models.FileField(verbose_name='Placement report', validators=[mentoring.validators.validate_size], blank=True, null=True, upload_to=mentoring.helpers.upload_to_placement_report)),
                ('report_uploaded_date', models.DateTimeField(blank=True, null=True)),
                ('certificate', models.FileField(verbose_name='Placement certificate', validators=[mentoring.validators.validate_size], blank=True, null=True, upload_to=mentoring.helpers.upload_to_placement_certificate)),
                ('state', models.CharField(verbose_name='State', choices=[('Not requested', 'Not requested'), ('Requested', 'Requested'), ('Mentoring denied', 'Mentoring denied'), ('Mentoring accepted', 'Mentoring accepted'), ('Seminar completed', 'Seminar completed'), ('Report accepted', 'Report accepted'), ('Certificate accepted', 'Certificate accepted'), ('Placement completed', 'Placement completed'), ('Placement failed', 'Placement failed'), ('Archived', 'Archived')], default='Not requested', max_length=100)),
                ('report_accepted', models.BooleanField(verbose_name='Report accepted', default=False)),
                ('certificate_accepted', models.BooleanField(verbose_name='Certificate accepted', default=False)),
            ],
            bases=('mentoring.abstractwork',),
        ),
        migrations.CreateModel(
            name='PortalUser',
            fields=[
                ('contactmodel_ptr', models.OneToOneField(to='mentoring.ContactModel', parent_link=True, auto_created=True)),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL, primary_key=True, serialize=False)),
            ],
            bases=('mentoring.contactmodel',),
        ),
        migrations.CreateModel(
            name='Thesis',
            fields=[
                ('abstractwork_ptr', models.OneToOneField(primary_key=True, to='mentoring.AbstractWork', auto_created=True, serialize=False, parent_link=True)),
                ('type', models.CharField(verbose_name='Type', choices=[('Bachelor', 'Bachelor'), ('Master', 'Master')], default='Bachelor', max_length=100)),
                ('second_examiner_first_name', models.CharField(verbose_name='First name', blank=True, null=True, max_length=30)),
                ('second_examiner_last_name', models.CharField(verbose_name='Last name', blank=True, null=True, max_length=30)),
                ('second_examiner_organisation', models.CharField(verbose_name='Organisation', blank=True, null=True, max_length=30)),
                ('second_examiner_title', models.CharField(verbose_name='title', blank=True, null=True, max_length=30)),
                ('expose', models.FileField(verbose_name='Expose', validators=[mentoring.validators.validate_size], blank=True, null=True, upload_to=mentoring.helpers.upload_to_thesis_expose)),
                ('poster', models.FileField(verbose_name='Poster', validators=[mentoring.validators.validate_size], blank=True, null=True, upload_to=mentoring.helpers.upload_to_thesis_poster)),
                ('thesis', models.FileField(verbose_name='Thesis', validators=[mentoring.validators.validate_size], blank=True, null=True, upload_to=mentoring.helpers.upload_to_thesis_thesis)),
                ('presentation', models.FileField(verbose_name='Presentation', blank=True, null=True, upload_to=mentoring.helpers.upload_to_thesis_presentation)),
                ('other', models.FileField(verbose_name='Other', blank=True, null=True, upload_to=mentoring.helpers.upload_to_thesis_other)),
                ('grade_first_examiner', models.DecimalField(verbose_name='Grade first examiner', max_digits=2, choices=[(Decimal('1.0'), '1,0'), (Decimal('1.3'), '1,3'), (Decimal('1.7'), '1,7'), (Decimal('2.0'), '2,0'), (Decimal('2.3'), '2,3'), (Decimal('2.7'), '2,7'), (Decimal('3.0'), '3,0'), (Decimal('3.3'), '3,3'), (Decimal('3.7'), '3,7'), (Decimal('4.0'), '4,0'), (Decimal('5.0'), '5,0')], blank=True, decimal_places=1, null=True)),
                ('grade_second_examiner', models.DecimalField(verbose_name='Grade second examiner', max_digits=2, choices=[(Decimal('1.0'), '1,0'), (Decimal('1.3'), '1,3'), (Decimal('1.7'), '1,7'), (Decimal('2.0'), '2,0'), (Decimal('2.3'), '2,3'), (Decimal('2.7'), '2,7'), (Decimal('3.0'), '3,0'), (Decimal('3.3'), '3,3'), (Decimal('3.7'), '3,7'), (Decimal('4.0'), '4,0'), (Decimal('5.0'), '5,0')], blank=True, decimal_places=1, null=True)),
                ('grade_presentation', models.DecimalField(verbose_name='Grade presentation', max_digits=2, choices=[(Decimal('1.0'), '1,0'), (Decimal('1.3'), '1,3'), (Decimal('1.7'), '1,7'), (Decimal('2.0'), '2,0'), (Decimal('2.3'), '2,3'), (Decimal('2.7'), '2,7'), (Decimal('3.0'), '3,0'), (Decimal('3.3'), '3,3'), (Decimal('3.7'), '3,7'), (Decimal('4.0'), '4,0'), (Decimal('5.0'), '5,0')], blank=True, decimal_places=1, null=True)),
                ('examination_office_state', models.CharField(verbose_name='Examination office state', choices=[('1A', 'Not submitted'), ('1B', 'Submitted'), ('2A', 'Accepted'), ('2B', 'Denied')], default='1A', max_length=100)),
                ('deadline', models.DateTimeField(verbose_name='Deadline', blank=True, null=True)),
                ('deadline_extended', models.BooleanField(verbose_name='Deadline extended', default=False)),
                ('colloquium_done', models.BooleanField(verbose_name='Colloquium done', default=False)),
                ('poster_printed', models.BooleanField(verbose_name='Poster printed', default=False)),
                ('poster_accepted', models.BooleanField(verbose_name='Poster accepted', default=False)),
                ('state', models.CharField(verbose_name='State', choices=[('Not requested', 'Not requested'), ('Requested', 'Requested'), ('Mentoring accepted', 'Mentoring accepted'), ('Mentoring denied', 'Mentoring denied'), ('Examination office submitted', 'Examination office submitted'), ('Examination office accepted', 'Examination office accepted'), ('Thesis submitted', 'Thesis submitted'), ('Colloquium completed', 'Colloquium completed'), ('Seminar completed', 'Seminar completed'), ('Poster accepted', 'Poster accepted'), ('Thesis completion', 'Thesis completion'), ('Thesis failed', 'Thesis failed'), ('Archived', 'Archived')], default='Not requested', max_length=100)),
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
            field=models.ManyToManyField(verbose_name='groups', to='auth.Group', related_name='user_set', blank=True, related_query_name='user', help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.'),
        ),
        migrations.AddField(
            model_name='mentoringuser',
            name='user_permissions',
            field=models.ManyToManyField(verbose_name='user permissions', to='auth.Permission', related_name='user_set', blank=True, related_query_name='user', help_text='Specific permissions for this user.'),
        ),
        migrations.CreateModel(
            name='PlacementCompanyContactData',
            fields=[
                ('contactdata_ptr', models.OneToOneField(primary_key=True, to='mentoring.ContactData', auto_created=True, serialize=False, parent_link=True)),
                ('placement', models.OneToOneField(to='mentoring.Placement', null=True)),
            ],
            bases=('mentoring.contactdata',),
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('portaluser_ptr', models.OneToOneField(primary_key=True, to='mentoring.PortalUser', auto_created=True, serialize=False, parent_link=True)),
                ('matriculation_number', models.CharField(verbose_name='Matriculation number', blank=True, null=True, max_length=8)),
                ('course', models.CharField(verbose_name='Course', choices=[('-', '-'), ('B-INF', 'B-INF'), ('M-INF', 'M-INF'), ('B-OSMI', 'B-OSMI'), ('M-OSMI', 'M-OSMI'), ('B-MEDINF', 'B-MEDINF'), ('B-ACS', 'B-ACS'), ('M-DM', 'M-DM')], default='-', max_length=30)),
                ('extern_email', models.EmailField(verbose_name='extern email address', blank=True, null=True, max_length=254)),
                ('placement_year', models.IntegerField(verbose_name='Placement year', blank=True, null=True)),
                ('bachelor_year', models.IntegerField(verbose_name='Bachelor year', blank=True, null=True)),
                ('master_year', models.IntegerField(verbose_name='Master year', blank=True, null=True)),
                ('placement_seminar_done', models.BooleanField(verbose_name='Placement seminar done', default=False)),
                ('bachelor_seminar_done', models.BooleanField(verbose_name='Bachelor seminar done', default=False)),
                ('master_seminar_done', models.BooleanField(verbose_name='Master seminar done', default=False)),
                ('bachelor_seminar_presentation_date', models.ForeignKey(to='mentoring.SeminarEntry', related_name='bachelor_seminar_presentation_student', blank=True, null=True)),
                ('master_seminar_presentation_date', models.ForeignKey(to='mentoring.SeminarEntry', related_name='master_seminar_presentation_student', blank=True, null=True)),
                ('placement_seminar_presentation_date', models.ForeignKey(to='mentoring.SeminarEntry', related_name='placement_seminar_presentation_student', blank=True, null=True)),
                ('seminar_entries', models.ManyToManyField(to='mentoring.SeminarEntry', related_name='seminar_students')),
            ],
            bases=('mentoring.portaluser',),
        ),
        migrations.CreateModel(
            name='Tutor',
            fields=[
                ('portaluser_ptr', models.OneToOneField(primary_key=True, to='mentoring.PortalUser', auto_created=True, serialize=False, parent_link=True)),
                ('placement_responsible', models.BooleanField(default=False)),
                ('thesis_responsible', models.BooleanField(default=False)),
                ('poster_responsible', models.BooleanField(default=False)),
            ],
            bases=('mentoring.portaluser',),
        ),
        migrations.AddField(
            model_name='studentactivethesis',
            name='thesis',
            field=models.OneToOneField(to='mentoring.Thesis', null=True),
        ),
        migrations.AddField(
            model_name='studentactiveplacement',
            name='placement',
            field=models.OneToOneField(to='mentoring.Placement', null=True),
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
