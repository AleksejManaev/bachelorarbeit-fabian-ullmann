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
                ('task', models.TextField(null=True, verbose_name='task')),
                ('updated_on', models.DateTimeField(auto_now=True, verbose_name='date updated', null=True)),
                ('sent_on', models.DateTimeField(null=True, verbose_name='date sent', blank=True)),
                ('comment_unread_by_student', models.BooleanField(default=False)),
                ('comment_unread_by_tutor', models.BooleanField(default=False)),
                ('mentoring_requested', models.BooleanField(default=False, verbose_name='Requested')),
                ('mentoring_accepted', models.CharField(default=b'ND', max_length=2, choices=[(b'ND', b'-'), (b'MA', b'Accepted'), (b'MD', b'Denied')])),
                ('completed', models.BooleanField(default=False, verbose_name='Completed')),
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
            name='Comment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('message', models.TextField(verbose_name='message')),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('private', models.BooleanField(default=False, verbose_name='Only visible for me')),
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
            name='PlacementSeminar',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('placement_year', models.IntegerField(unique=True, null=True, verbose_name='Placement year', blank=True)),
            ],
            options={
                'verbose_name': 'Placement seminar',
            },
        ),
        migrations.CreateModel(
            name='PlacementSeminarEntry',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateTimeField()),
                ('placement_seminar', models.ForeignKey(to='mentoring.PlacementSeminar')),
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
            name='ContactData',
            fields=[
                ('contactmodel_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='mentoring.ContactModel')),
                ('first_name', models.CharField(max_length=30, null=True, verbose_name='First name', blank=True)),
                ('last_name', models.CharField(max_length=30, null=True, verbose_name='Last name', blank=True)),
                ('email', models.EmailField(max_length=254, null=True, verbose_name='Email', blank=True)),
            ],
            bases=('mentoring.contactmodel',),
        ),
        migrations.CreateModel(
            name='Placement',
            fields=[
                ('abstractwork_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='mentoring.AbstractWork')),
                ('company_name', models.CharField(max_length=100, null=True, verbose_name='company name', blank=True)),
                ('company_address', models.TextField(null=True, verbose_name='company address', blank=True)),
                ('date_from', models.DateField(null=True, verbose_name='internship begin', blank=True)),
                ('date_to', models.DateField(null=True, verbose_name='internship end', blank=True)),
                ('report', models.FileField(blank=True, upload_to=mentoring.helpers.upload_to_placement_report, null=True, verbose_name='Placement report', validators=[mentoring.validators.validate_pdf, mentoring.validators.validate_size])),
                ('report_uploaded_date', models.DateTimeField(null=True, blank=True)),
                ('certificate', models.FileField(blank=True, upload_to=mentoring.helpers.upload_to_placement_certificate, null=True, verbose_name='Placement certificate', validators=[mentoring.validators.validate_pdf, mentoring.validators.validate_size])),
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
                ('type', models.CharField(default=b'Bachelor', max_length=100, verbose_name='Type', choices=[(b'Bachelor', b'Bachelor'), (b'Master', b'Master')])),
                ('second_examiner_first_name', models.CharField(max_length=30, null=True, verbose_name='First name', blank=True)),
                ('second_examiner_last_name', models.CharField(max_length=30, null=True, verbose_name='Last name', blank=True)),
                ('second_examiner_organisation', models.CharField(max_length=30, null=True, verbose_name='Organisation', blank=True)),
                ('second_examiner_title', models.CharField(max_length=30, null=True, verbose_name='title', blank=True)),
                ('poster', models.FileField(blank=True, upload_to=mentoring.helpers.upload_to_thesis_poster, null=True, verbose_name='Poster', validators=[mentoring.validators.validate_pdf, mentoring.validators.validate_size])),
                ('thesis', models.FileField(blank=True, upload_to=mentoring.helpers.upload_to_thesis_thesis, null=True, verbose_name='Thesis', validators=[mentoring.validators.validate_pdf, mentoring.validators.validate_size])),
                ('presentation', models.FileField(upload_to=mentoring.helpers.upload_to_thesis_presentation, null=True, verbose_name='Presentation', blank=True)),
                ('other', models.FileField(upload_to=mentoring.helpers.upload_to_thesis_other, null=True, verbose_name='Other', blank=True)),
                ('grade_first_examiner', models.CharField(default=b'-', max_length=3, verbose_name='Grade first examiner', choices=[(b'-', b'-'), (b'1,0', b'1,0'), (b'1,3', b'1,3'), (b'1,7', b'1,7'), (b'2,0', b'2,0'), (b'2,3', b'2,3'), (b'3,0', b'3,0'), (b'3,3', b'3,3'), (b'3,7', b'3,7'), (b'4,0', b'4,0'), (b'5,0', b'5,0')])),
                ('grade_second_examiner', models.CharField(default=b'-', max_length=3, verbose_name='Grade second examiner', choices=[(b'-', b'-'), (b'1,0', b'1,0'), (b'1,3', b'1,3'), (b'1,7', b'1,7'), (b'2,0', b'2,0'), (b'2,3', b'2,3'), (b'3,0', b'3,0'), (b'3,3', b'3,3'), (b'3,7', b'3,7'), (b'4,0', b'4,0'), (b'5,0', b'5,0')])),
                ('grade_presentation', models.CharField(default=b'-', max_length=3, verbose_name='Grade presentation', choices=[(b'-', b'-'), (b'1,0', b'1,0'), (b'1,3', b'1,3'), (b'1,7', b'1,7'), (b'2,0', b'2,0'), (b'2,3', b'2,3'), (b'3,0', b'3,0'), (b'3,3', b'3,3'), (b'3,7', b'3,7'), (b'4,0', b'4,0'), (b'5,0', b'5,0')])),
                ('examination_office_state', models.CharField(default=b'1A', max_length=100, verbose_name='Examination office state', choices=[(b'1A', b'Not sent'), (b'1B', b'Sent'), (b'2A', b'Accepted'), (b'2B', b'Denied')])),
                ('deadline', models.DateTimeField(null=True, verbose_name='Deadline', blank=True)),
                ('deadline_extended', models.BooleanField(default=False, verbose_name='Deadline extended')),
                ('colloquium_done', models.BooleanField(default=False, verbose_name='Colloquium done')),
            ],
            bases=('mentoring.abstractwork',),
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
            field=models.ManyToManyField(related_query_name='user', related_name='user_set', to='auth.Group', blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', verbose_name='groups'),
        ),
        migrations.AddField(
            model_name='mentoringuser',
            name='user_permissions',
            field=models.ManyToManyField(related_query_name='user', related_name='user_set', to='auth.Permission', blank=True, help_text='Specific permissions for this user.', verbose_name='user permissions'),
        ),
        migrations.CreateModel(
            name='PlacementCompanyContactData',
            fields=[
                ('contactdata_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='mentoring.ContactData')),
                ('placement', models.OneToOneField(null=True, to='mentoring.Placement')),
            ],
            bases=('mentoring.contactdata',),
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('portaluser_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='mentoring.PortalUser')),
                ('matriculation_number', models.CharField(max_length=8, null=True, verbose_name='Matriculation number', blank=True)),
                ('course', models.CharField(default=b'-', max_length=30, verbose_name='course placement', choices=[(b'-', b'-'), (b'B-INF', b'B-INF'), (b'M-INF', b'M-INF'), (b'B-OSMI', b'B-OSMI'), (b'M-OSMI', b'M-OSMI'), (b'B-MEDINF', b'B-MEDINF'), (b'B-ACS', b'B-ACS'), (b'M-DM', b'M-DM')])),
                ('extern_email', models.EmailField(max_length=254, null=True, verbose_name='extern email address', blank=True)),
                ('placement_year', models.IntegerField(null=True, verbose_name='Placement year', blank=True)),
                ('placement_seminar_done', models.BooleanField(default=False, verbose_name='Placement seminar done')),
                ('placement_seminar_entries', models.ManyToManyField(related_name='seminar_students', to='mentoring.PlacementSeminarEntry', blank=True)),
                ('presentation_date', models.ForeignKey(related_name='presentation_student', blank=True, to='mentoring.PlacementSeminarEntry', null=True)),
            ],
            bases=('mentoring.portaluser',),
        ),
        migrations.CreateModel(
            name='Tutor',
            fields=[
                ('portaluser_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='mentoring.PortalUser')),
                ('placement_responsible', models.BooleanField(default=False)),
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
