# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import mentoring.helpers
from decimal import Decimal
import django.core.validators
import django.contrib.auth.models
import mentoring.validators
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0006_require_contenttypes_0002'),
    ]

    operations = [
        migrations.CreateModel(
            name='MentoringUser',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(help_text='Designates that this user has all permissions without explicitly assigning them.', default=False, verbose_name='superuser status')),
                ('username', models.CharField(max_length=30, unique=True, error_messages={'unique': 'A user with that username already exists.'}, validators=[django.core.validators.RegexValidator('^[\\w.@+-]+$', 'Enter a valid username. This value may contain only letters, numbers and @/./+/-/_ characters.', 'invalid')], help_text='Required. 30 characters or fewer. Letters, digits and @/./+/-/_ only.', verbose_name='username')),
                ('first_name', models.CharField(max_length=30, blank=True, verbose_name='first name')),
                ('last_name', models.CharField(max_length=30, blank=True, verbose_name='last name')),
                ('email', models.EmailField(max_length=254, blank=True, verbose_name='email address')),
                ('is_staff', models.BooleanField(help_text='Designates whether the user can log into this admin site.', default=False, verbose_name='staff status')),
                ('is_active', models.BooleanField(help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', default=True, verbose_name='active')),
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
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('created_on', models.DateTimeField(auto_created=True, verbose_name='date joined', auto_now_add=True)),
                ('task', models.TextField(null=True, verbose_name='task')),
                ('updated_on', models.DateTimeField(auto_now=True, null=True, verbose_name='date updated')),
                ('sent_on', models.DateTimeField(blank=True, null=True, verbose_name='date sent')),
                ('comment_unread_by_student', models.BooleanField(default=False)),
                ('comment_unread_by_tutor', models.BooleanField(default=False)),
                ('mentoring_requested', models.BooleanField(default=False, verbose_name='Requested')),
                ('mentoring_accepted', models.CharField(max_length=2, choices=[('ND', '-'), ('MA', 'Accepted'), ('MD', 'Denied')], default='ND')),
                ('archived', models.BooleanField(default=False, verbose_name='Archived')),
                ('completed', models.CharField(max_length=100, choices=[('-', '-'), ('Completed', 'Completed'), ('Failed', 'Failed')], default='-', verbose_name='Completed')),
            ],
        ),
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('street', models.CharField(max_length=255, blank=True, null=True, verbose_name='street')),
                ('zip_code', models.CharField(max_length=30, blank=True, null=True, verbose_name='zip code')),
                ('location', models.CharField(max_length=100, blank=True, null=True, verbose_name='location')),
                ('web_address', models.CharField(max_length=255, blank=True, null=True, verbose_name='web address')),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('message', models.TextField(verbose_name='message')),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('private', models.BooleanField(default=False, verbose_name='Only visible for me')),
            ],
        ),
        migrations.CreateModel(
            name='ContactModel',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('title', models.CharField(max_length=30, blank=True, null=True, verbose_name='title')),
                ('phone', models.CharField(max_length=30, blank=True, null=True, verbose_name='phone')),
            ],
        ),
        migrations.CreateModel(
            name='Seminar',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('year', models.IntegerField(blank=True, null=True, verbose_name='Year')),
                ('type', models.CharField(max_length=10, choices=[('placement', 'placement'), ('bachelor', 'bachelor'), ('master', 'master')], verbose_name='Seminar type')),
            ],
            options={
                'verbose_name': 'Seminar',
            },
        ),
        migrations.CreateModel(
            name='SeminarEntry',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('date', models.DateTimeField()),
                ('seminar', models.ForeignKey(to='mentoring.Seminar')),
            ],
        ),
        migrations.CreateModel(
            name='StudentActivePlacement',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
            ],
        ),
        migrations.CreateModel(
            name='StudentActiveThesis',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
            ],
        ),
        migrations.CreateModel(
            name='ContactData',
            fields=[
                ('contactmodel_ptr', models.OneToOneField(auto_created=True, parent_link=True, to='mentoring.ContactModel', serialize=False, primary_key=True)),
                ('first_name', models.CharField(max_length=30, blank=True, null=True, verbose_name='First name')),
                ('last_name', models.CharField(max_length=30, blank=True, null=True, verbose_name='Last name')),
                ('email', models.EmailField(max_length=254, blank=True, null=True, verbose_name='Email')),
            ],
            bases=('mentoring.contactmodel',),
        ),
        migrations.CreateModel(
            name='Placement',
            fields=[
                ('abstractwork_ptr', models.OneToOneField(auto_created=True, parent_link=True, to='mentoring.AbstractWork', serialize=False, primary_key=True)),
                ('company_name', models.CharField(max_length=100, blank=True, null=True, verbose_name='company name')),
                ('company_address', models.TextField(blank=True, null=True, verbose_name='company address')),
                ('date_from', models.DateField(blank=True, null=True, verbose_name='internship begin')),
                ('date_to', models.DateField(blank=True, null=True, verbose_name='internship end')),
                ('report', models.FileField(upload_to=mentoring.helpers.upload_to_placement_report, null=True, validators=[mentoring.validators.validate_size], blank=True, verbose_name='Placement report')),
                ('report_uploaded_date', models.DateTimeField(blank=True, null=True)),
                ('certificate', models.FileField(upload_to=mentoring.helpers.upload_to_placement_certificate, null=True, validators=[mentoring.validators.validate_size], blank=True, verbose_name='Placement certificate')),
                ('state', models.CharField(max_length=100, choices=[('Not requested', 'Not requested'), ('Requested', 'Requested'), ('Mentoring denied', 'Mentoring denied'), ('Mentoring accepted', 'Mentoring accepted'), ('Seminar completed', 'Seminar completed'), ('Report accepted', 'Report accepted'), ('Certificate accepted', 'Certificate accepted'), ('Placement completed', 'Placement completed'), ('Placement failed', 'Placement failed'), ('Archived', 'Archived')], default='Not requested', verbose_name='State')),
                ('report_accepted', models.BooleanField(default=False, verbose_name='Report accepted')),
                ('certificate_accepted', models.BooleanField(default=False, verbose_name='Certificate accepted')),
            ],
            bases=('mentoring.abstractwork',),
        ),
        migrations.CreateModel(
            name='PortalUser',
            fields=[
                ('contactmodel_ptr', models.OneToOneField(auto_created=True, parent_link=True, to='mentoring.ContactModel')),
                ('user', models.OneToOneField(primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
            ],
            bases=('mentoring.contactmodel',),
        ),
        migrations.CreateModel(
            name='Thesis',
            fields=[
                ('abstractwork_ptr', models.OneToOneField(auto_created=True, parent_link=True, to='mentoring.AbstractWork', serialize=False, primary_key=True)),
                ('type', models.CharField(max_length=100, choices=[('Bachelor', 'Bachelor'), ('Master', 'Master')], default='Bachelor', verbose_name='Type')),
                ('second_examiner_first_name', models.CharField(max_length=30, blank=True, null=True, verbose_name='First name')),
                ('second_examiner_last_name', models.CharField(max_length=30, blank=True, null=True, verbose_name='Last name')),
                ('second_examiner_organisation', models.CharField(max_length=30, blank=True, null=True, verbose_name='Organisation')),
                ('second_examiner_title', models.CharField(max_length=30, blank=True, null=True, verbose_name='title')),
                ('expose', models.FileField(upload_to=mentoring.helpers.upload_to_thesis_expose, null=True, validators=[mentoring.validators.validate_size], blank=True, verbose_name='Expose')),
                ('poster', models.FileField(upload_to=mentoring.helpers.upload_to_thesis_poster, null=True, validators=[mentoring.validators.validate_size], blank=True, verbose_name='Poster')),
                ('thesis', models.FileField(upload_to=mentoring.helpers.upload_to_thesis_thesis, null=True, validators=[mentoring.validators.validate_size], blank=True, verbose_name='Thesis')),
                ('presentation', models.FileField(upload_to=mentoring.helpers.upload_to_thesis_presentation, blank=True, null=True, verbose_name='Presentation')),
                ('other', models.FileField(upload_to=mentoring.helpers.upload_to_thesis_other, blank=True, null=True, verbose_name='Other')),
                ('grade_first_examiner', models.DecimalField(choices=[(Decimal('1.0'), '1,0'), (Decimal('1.3'), '1,3'), (Decimal('1.7'), '1,7'), (Decimal('2.0'), '2,0'), (Decimal('2.3'), '2,3'), (Decimal('2.7'), '2,7'), (Decimal('3.0'), '3,0'), (Decimal('3.3'), '3,3'), (Decimal('3.7'), '3,7'), (Decimal('4.0'), '4,0'), (Decimal('5.0'), '5,0')], decimal_places=1, max_digits=2, null=True, blank=True, verbose_name='Grade first examiner')),
                ('grade_second_examiner', models.DecimalField(choices=[(Decimal('1.0'), '1,0'), (Decimal('1.3'), '1,3'), (Decimal('1.7'), '1,7'), (Decimal('2.0'), '2,0'), (Decimal('2.3'), '2,3'), (Decimal('2.7'), '2,7'), (Decimal('3.0'), '3,0'), (Decimal('3.3'), '3,3'), (Decimal('3.7'), '3,7'), (Decimal('4.0'), '4,0'), (Decimal('5.0'), '5,0')], decimal_places=1, max_digits=2, null=True, blank=True, verbose_name='Grade second examiner')),
                ('grade_presentation', models.DecimalField(choices=[(Decimal('1.0'), '1,0'), (Decimal('1.3'), '1,3'), (Decimal('1.7'), '1,7'), (Decimal('2.0'), '2,0'), (Decimal('2.3'), '2,3'), (Decimal('2.7'), '2,7'), (Decimal('3.0'), '3,0'), (Decimal('3.3'), '3,3'), (Decimal('3.7'), '3,7'), (Decimal('4.0'), '4,0'), (Decimal('5.0'), '5,0')], decimal_places=1, max_digits=2, null=True, blank=True, verbose_name='Grade presentation')),
                ('examination_office_state', models.CharField(max_length=100, choices=[('1A', 'Not submitted'), ('1B', 'Submitted'), ('2A', 'Accepted'), ('2B', 'Denied')], default='1A', verbose_name='Examination office state')),
                ('deadline', models.DateTimeField(blank=True, null=True, verbose_name='Deadline')),
                ('deadline_extended', models.BooleanField(default=False, verbose_name='Deadline extended')),
                ('colloquium_done', models.BooleanField(default=False, verbose_name='Colloquium done')),
                ('poster_printed', models.BooleanField(default=False, verbose_name='Poster printed')),
                ('poster_accepted', models.BooleanField(default=False, verbose_name='Poster accepted')),
                ('state', models.CharField(max_length=100, choices=[('Not requested', 'Not requested'), ('Requested', 'Requested'), ('Mentoring accepted', 'Mentoring accepted'), ('Mentoring denied', 'Mentoring denied'), ('Examination office submitted', 'Examination office submitted'), ('Examination office accepted', 'Examination office accepted'), ('Thesis submitted', 'Thesis submitted'), ('Colloquium completed', 'Colloquium completed'), ('Seminar completed', 'Seminar completed'), ('Poster accepted', 'Poster accepted'), ('Thesis completed', 'Thesis completed'), ('Thesis failed', 'Thesis failed'), ('Archived', 'Archived')], default='Not requested', verbose_name='State')),
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
            field=models.ManyToManyField(related_query_name='user', related_name='user_set', help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', blank=True, verbose_name='groups', to='auth.Group'),
        ),
        migrations.AddField(
            model_name='mentoringuser',
            name='user_permissions',
            field=models.ManyToManyField(related_query_name='user', related_name='user_set', help_text='Specific permissions for this user.', blank=True, verbose_name='user permissions', to='auth.Permission'),
        ),
        migrations.CreateModel(
            name='PlacementCompanyContactData',
            fields=[
                ('contactdata_ptr', models.OneToOneField(auto_created=True, parent_link=True, to='mentoring.ContactData', serialize=False, primary_key=True)),
                ('placement', models.OneToOneField(null=True, to='mentoring.Placement')),
            ],
            bases=('mentoring.contactdata',),
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('portaluser_ptr', models.OneToOneField(auto_created=True, parent_link=True, to='mentoring.PortalUser', serialize=False, primary_key=True)),
                ('matriculation_number', models.CharField(max_length=8, blank=True, null=True, verbose_name='Matriculation number')),
                ('course', models.CharField(max_length=30, choices=[('-', '-'), ('B-INF', 'B-INF'), ('M-INF', 'M-INF'), ('B-OSMI', 'B-OSMI'), ('M-OSMI', 'M-OSMI'), ('B-MEDINF', 'B-MEDINF'), ('B-ACS', 'B-ACS'), ('M-DM', 'M-DM')], default='-', verbose_name='Course')),
                ('extern_email', models.EmailField(max_length=254, blank=True, null=True, verbose_name='extern email address')),
                ('placement_year', models.IntegerField(blank=True, null=True, verbose_name='Placement year')),
                ('bachelor_year', models.IntegerField(blank=True, null=True, verbose_name='Bachelor year')),
                ('master_year', models.IntegerField(blank=True, null=True, verbose_name='Master year')),
                ('placement_seminar_done', models.BooleanField(default=False, verbose_name='Placement seminar done')),
                ('bachelor_seminar_done', models.BooleanField(default=False, verbose_name='Bachelor seminar done')),
                ('master_seminar_done', models.BooleanField(default=False, verbose_name='Master seminar done')),
                ('bachelor_seminar_presentation_date', models.ForeignKey(null=True, blank=True, related_name='bachelor_seminar_presentation_student', to='mentoring.SeminarEntry')),
                ('master_seminar_presentation_date', models.ForeignKey(null=True, blank=True, related_name='master_seminar_presentation_student', to='mentoring.SeminarEntry')),
                ('placement_seminar_presentation_date', models.ForeignKey(null=True, blank=True, related_name='placement_seminar_presentation_student', to='mentoring.SeminarEntry')),
                ('seminar_entries', models.ManyToManyField(related_name='seminar_students', blank=True, null=True, to='mentoring.SeminarEntry')),
            ],
            bases=('mentoring.portaluser',),
        ),
        migrations.CreateModel(
            name='Tutor',
            fields=[
                ('portaluser_ptr', models.OneToOneField(auto_created=True, parent_link=True, to='mentoring.PortalUser', serialize=False, primary_key=True)),
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
            field=models.ForeignKey(null=True, to='mentoring.Student'),
        ),
        migrations.AddField(
            model_name='abstractwork',
            name='tutor',
            field=models.ForeignKey(null=True, to='mentoring.Tutor'),
        ),
    ]
