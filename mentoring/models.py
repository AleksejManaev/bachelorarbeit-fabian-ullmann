# -*- coding: utf-8 -*-
import os
from decimal import Decimal

import pytz
from django.contrib.auth.models import AbstractUser
from django.template.defaultfilters import date
from django.utils.encoding import python_2_unicode_compatible
from django.utils.timezone import localtime
from django.utils.translation import ugettext_lazy as _

from mentoring.helpers import *
from mentoring.validators import *

app_label = 'mentoring'

PLACEMENT_STATE_CHOICES = (
    ('Not requested', _('Not requested')),
    ('Requested', _('Requested')),
    ('Mentoring denied', _('Mentoring denied')),
    ('Mentoring accepted', _('Mentoring accepted')),
    ('Seminar completed', _('Seminar completed')),
    ('Report accepted', _('Report accepted')),
    ('Certificate accepted', _('Certificate accepted')),
    ('Placement completed', _('Placement completed')),
    ('Placement failed', _('Placement failed')),
    ('Archived', _('Archived'))
)

THESIS_STATE_CHOICES = (
    ('Not requested', _('Not requested')),
    ('Requested', _('Requested')),
    ('Mentoring accepted', _('Mentoring accepted')),
    ('Mentoring denied', _('Mentoring denied')),
    ('Examination office submitted', _('Examination office submitted')),
    ('Examination office accepted', _('Examination office accepted')),
    ('Thesis submitted', _('Thesis submitted')),
    ('Colloquium completed', _('Colloquium completed')),
    ('Seminar completed', _('Seminar completed')),
    ('Poster accepted', _('Poster accepted')),
    ('Thesis completed', _('Thesis completed')),
    ('Thesis failed', _('Thesis failed')),
    ('Archived', _('Archived'))
)

ABSTRACTWORK_COMPLETED_CHOICES = (
    ('-', '-'),
    ('Completed', _('Completed')),
    ('Failed', _('Failed'))
)

PLACEMENT_STATE_SUBGOAL_CHOICES = (
    ('Requested', _('Mentoring acceptance')),
    ('Mentoring accepted', _('Seminar completion')),
    ('Mentoring denied', _('-')),
    ('Seminar completed', _('Report acceptance')),
    ('Report accepted', _('Certificate acceptance')),
    ('Certificate accepted', _('Placement completion')),
    ('Placement completed', _('-')),
    ('Placement failed', _('-')),
    ('Archived', _('-'))
)

THESIS_STATE_SUBGOAL_CHOICES = (
    ('Requested', _('Mentoring acceptance')),
    ('Mentoring accepted', _('Examination office submitted')),
    ('Mentoring denied', _('-')),
    ('Examination office submitted', _('Examination office accepted')),
    ('Examination office accepted', _('Thesis submitted')),
    ('Thesis submitted', _('Colloquium completed')),
    ('Colloquium completed', _('Seminar completed')),
    ('Seminar completed', _('Poster accepted')),
    ('Poster accepted', _('Thesis completed')),
    ('Thesis completed', _('-')),
    ('Thesis failed', _('-')),
    ('Archived', _('-'))
)

MENTORING_STATE_CHOICES = (
    ('ND', '-'),
    ('MA', _('Accepted')),
    ('MD', _('Denied')),
)

THESIS_CHOICES = (
    ('Bachelor', 'Bachelor'),
    ('Master', 'Master'),
)

GRADE_CHOICES = (
    (Decimal('1.0'), '1,0'),
    (Decimal('1.3'), '1,3'),
    (Decimal('1.7'), '1,7'),
    (Decimal('2.0'), '2,0'),
    (Decimal('2.3'), '2,3'),
    (Decimal('2.7'), '2,7'),
    (Decimal('3.0'), '3,0'),
    (Decimal('3.3'), '3,3'),
    (Decimal('3.7'), '3,7'),
    (Decimal('4.0'), '4,0'),
    (Decimal('5.0'), '5,0')
)

EXAMINATION_OFFICE_STATE_CHOICES = (
    ('1A', _('Not submitted')),
    ('1B', _('Submitted')),
    ('2A', _('Accepted')),
    ('2B', _('Denied'))
)

COURSE_CHOICES = (
    ('-', '-'),
    ('B-INF', 'B-INF'),
    ('M-INF', 'M-INF'),
    ('B-OSMI', 'B-OSMI'),
    ('M-OSMI', 'M-OSMI'),
    ('B-MEDINF', 'B-MEDINF'),
    ('B-ACS', 'B-ACS'),
    ('M-DM', 'M-DM')
)

SEMINAR_TYPE_CHOICES = (
    ('placement', _('placement')),
    ('bachelor', _('bachelor')),
    ('master', _('master')),
)


class MentoringUser(AbstractUser):
    gidNumber = models.IntegerField(null=True)


class ContactModel(models.Model):
    title = models.CharField(_('title'), max_length=30, null=True, blank=True)
    phone = models.CharField(_('phone'), max_length=30, blank=True, null=True)


class PortalUser(ContactModel):
    user = models.OneToOneField(MentoringUser, primary_key=True, verbose_name=_('user'))


@python_2_unicode_compatible
class Tutor(PortalUser):
    placement_responsible = models.BooleanField(default=False, null=False, blank=False, verbose_name=_('Placement responsible'))
    thesis_responsible = models.BooleanField(default=False, null=False, blank=False, verbose_name=_('Thesis responsible'))
    poster_responsible = models.BooleanField(default=False, null=False, blank=False, verbose_name=_('Poster responsible'))

    class Meta:
        verbose_name = _('Tutor')
        verbose_name_plural = _('Tutors')

    @property
    def get_full_name(self):
        return "%s %s %s" % (self.title or '', self.user.first_name or '', self.user.last_name or '')

    def __str__(self):
        return u"{} {} {}".format(self.title or '', self.user.first_name or '', self.user.last_name or '')


class Seminar(models.Model):
    year = models.IntegerField(_('Year'), blank=True, null=True)
    type = models.CharField(_('Seminar type'), max_length=10, choices=SEMINAR_TYPE_CHOICES)

    class Meta:
        verbose_name = _('Seminar')
        verbose_name_plural = _('Seminars')
        unique_together = ('year', 'type')

    def __str__(self):
        return "{} {}".format(self.year or '', _(self.type) or '')


class SeminarEntry(models.Model):
    date = models.DateTimeField(verbose_name=_('Date'))
    seminar = models.ForeignKey(Seminar)

    class Meta:
        verbose_name = _('Seminar entry')
        verbose_name_plural = _('Seminar entries')

    def __str__(self):
        return "{} - {}".format(date(localtime(self.date), 'SHORT_DATE_FORMAT') or '', self.seminar.__str__() or '')


@python_2_unicode_compatible
class Student(PortalUser):
    matriculation_number = models.CharField(_('Matriculation number'), max_length=8, null=True, blank=True)
    course = models.CharField(_('Course'), max_length=30, choices=COURSE_CHOICES, default='-')
    extern_email = models.EmailField(_('extern email address'), null=True, blank=True)
    placement_year = models.IntegerField(_('Placement year'), blank=True, null=True)
    bachelor_year = models.IntegerField(_('Bachelor year'), blank=True, null=True)
    master_year = models.IntegerField(_('Master year'), blank=True, null=True)
    placement_seminar_presentation_date = models.ForeignKey(SeminarEntry, blank=True, null=True, related_name='placement_seminar_presentation_student', verbose_name='{} - {}'.format(_('Seminar presentation date'), _('Placement')))
    bachelor_seminar_presentation_date = models.ForeignKey(SeminarEntry, blank=True, null=True, related_name='bachelor_seminar_presentation_student', verbose_name='{} - {}'.format(_('Seminar presentation date'), _('Bachelor')))
    master_seminar_presentation_date = models.ForeignKey(SeminarEntry, blank=True, null=True, related_name='master_seminar_presentation_student', verbose_name='{} - {}'.format(_('Seminar presentation date'), _('Master')))
    placement_seminar_done = models.BooleanField(_('Placement seminar done'), default=False)
    bachelor_seminar_done = models.BooleanField(_('Bachelor seminar done'), default=False)
    master_seminar_done = models.BooleanField(_('Master seminar done'), default=False)
    seminar_entries = models.ManyToManyField(SeminarEntry, blank=True, null=True, related_name='seminar_students', verbose_name=_('Seminar entries'))

    class Meta:
        verbose_name = _('Student')
        verbose_name_plural = _('Students')

    def __str__(self):
        return u"{} ({})".format(self.user.get_full_name() or '', self.matriculation_number or '')


class Address(models.Model):
    student = models.OneToOneField(Student)
    street = models.CharField(_('street'), max_length=255, blank=True, null=True)
    zip_code = models.CharField(_('zip code'), max_length=30, blank=True, null=True)
    location = models.CharField(_('location'), max_length=100, blank=True, null=True)
    web_address = models.CharField(_('web address'), max_length=255, blank=True, null=True)

    class Meta:
        verbose_name = _('Address')
        verbose_name_plural = _('Addresses')

    def __str__(self):
        return self.student.__str__()


class AbstractWork(models.Model):
    student = models.ForeignKey(Student, null=True)
    tutor = models.ForeignKey(Tutor, null=True)
    task = models.TextField(_('task'), null=True)
    created_on = models.DateTimeField(_('date joined'), auto_created=True, auto_now_add=True)
    updated_on = models.DateTimeField(_('date updated'), auto_now=True, null=True)
    sent_on = models.DateTimeField(_('date sent'), blank=True, null=True)
    comment_unread_by_student = models.BooleanField(_('Comment unread by student'), default=False)
    comment_unread_by_tutor = models.BooleanField(_('Comment unread by tutor'), default=False)
    mentoring_requested = models.BooleanField(_('Requested'), default=False)
    mentoring_accepted = models.CharField(_('Mentoring accepted'), max_length=2, choices=MENTORING_STATE_CHOICES, default='ND')
    archived = models.BooleanField(_('Archived'), default=False)
    completed = models.CharField(_('Completed'), choices=ABSTRACTWORK_COMPLETED_CHOICES, max_length=100, default='-')

    def __str__(self):
        return "{}".format(self.task if self.task else _('No task'))


@python_2_unicode_compatible
class Placement(AbstractWork):
    company_name = models.CharField(_('company name'), max_length=100, null=True, blank=True)
    company_address = models.TextField(_('company address'), null=True, blank=True)
    date_from = models.DateField(_('internship begin'), blank=True, null=True)
    date_to = models.DateField(_('internship end'), blank=True, null=True)
    report = models.FileField(_('Placement report'), upload_to=upload_to_placement_report, blank=True, null=True, validators=[validate_size])
    report_uploaded_date = models.DateTimeField(blank=True, null=True)
    certificate = models.FileField(_('Placement certificate'), upload_to=upload_to_placement_certificate, blank=True, null=True, validators=[validate_size])
    state = models.CharField(_('State'), choices=PLACEMENT_STATE_CHOICES, max_length=100, default='Not requested')
    report_accepted = models.BooleanField(_('Report accepted'), default=False)
    certificate_accepted = models.BooleanField(_('Certificate accepted'), default=False)

    class Meta:
        verbose_name = _('Placement')
        verbose_name_plural = _('Placements')

    def __str__(self):
        return super(Placement, self).__str__()

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        super(Placement, self).save(force_insert, force_update, using, update_fields)

        # Loeschen alter Upload-Dateien
        for object in [self.report, self.certificate]:
            if (bool(object)):
                dir = os.path.dirname(getattr(object, 'path'))
                for file in os.listdir(dir):
                    samefile = os.path.samefile(getattr(object, 'path'), os.path.join(dir, file))
                    if not samefile:
                        os.remove(os.path.join(dir, file))


class StudentActivePlacement(models.Model):
    student = models.OneToOneField(Student, verbose_name=_('Student'))
    placement = models.OneToOneField(Placement, verbose_name=_('Placement'), null=True)

    class Meta:
        verbose_name = _('Active placement')
        verbose_name_plural = _('Active placements')

    def __str__(self):
        return '{} - {}'.format(self.student, self.placement.__str__())


class Thesis(AbstractWork):
    type = models.CharField(_('Type'), max_length=100, choices=THESIS_CHOICES, default='Bachelor')
    second_examiner_first_name = models.CharField(_('First name'), max_length=30, null=True, blank=True)
    second_examiner_last_name = models.CharField(_('Last name'), max_length=30, null=True, blank=True)
    second_examiner_organisation = models.CharField(_('Organisation'), max_length=30, null=True, blank=True)
    second_examiner_title = models.CharField(_('title'), max_length=30, null=True, blank=True)
    expose = models.FileField(_('Expose'), upload_to=upload_to_thesis_expose, blank=True, null=True, validators=[validate_size])
    poster = models.FileField(_('Poster'), upload_to=upload_to_thesis_poster, blank=True, null=True, validators=[validate_size])
    thesis = models.FileField(_('Thesis'), upload_to=upload_to_thesis_thesis, blank=True, null=True, validators=[validate_size])
    presentation = models.FileField(_('Presentation'), upload_to=upload_to_thesis_presentation, blank=True, null=True)
    other = models.FileField(_('Other'), upload_to=upload_to_thesis_other, blank=True, null=True)
    grade_first_examiner = models.DecimalField(_('Grade first examiner'), choices=GRADE_CHOICES, blank=True, null=True, decimal_places=1, max_digits=2)
    grade_second_examiner = models.DecimalField(_('Grade second examiner'), choices=GRADE_CHOICES, blank=True, null=True, decimal_places=1, max_digits=2)
    grade_presentation = models.DecimalField(_('Grade presentation'), choices=GRADE_CHOICES, blank=True, null=True, decimal_places=1, max_digits=2)
    examination_office_state = models.CharField(_('Examination office state'), max_length=100, choices=EXAMINATION_OFFICE_STATE_CHOICES, default='1A')
    deadline = models.DateTimeField(_('Deadline'), null=True, blank=True)
    deadline_extended = models.BooleanField(_('Deadline extended'), default=False)
    colloquium_done = models.BooleanField(_('Colloquium done'), default=False)
    poster_printed = models.BooleanField(_('Poster printed'), default=False)
    poster_accepted = models.BooleanField(_('Poster accepted'), default=False)
    state = models.CharField(_('State'), choices=THESIS_STATE_CHOICES, max_length=100, default='Not requested')

    class Meta:
        verbose_name = _('Thesis')
        verbose_name_plural = _('Theses')

    def __str__(self):
        return super(Thesis, self).__str__()

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        # Zeitzone anpassen und somit den richtigen Tag setzen
        deadline = getattr(self, 'deadline')
        if deadline:
            self.deadline = deadline.replace(tzinfo=pytz.timezone('UTC'))

        super(Thesis, self).save(force_insert, force_update, using, update_fields)

        # Loeschen alter Upload-Dateien
        for object in [self.expose, self.thesis, self.poster, self.presentation, self.other]:
            if (bool(object)):
                dir = os.path.dirname(getattr(object, 'path'))
                for file in os.listdir(dir):
                    samefile = os.path.samefile(getattr(object, 'path'), os.path.join(dir, file))
                    if not samefile:
                        os.remove(os.path.join(dir, file))


class StudentActiveThesis(models.Model):
    student = models.OneToOneField(Student, verbose_name=_('Student'))
    thesis = models.OneToOneField(Thesis, verbose_name=_('Thesis'), null=True)

    class Meta:
        verbose_name = _('Active Thesis')
        verbose_name_plural = _('Active Theses')

    def __str__(self):
        return '{} - {}'.format(self.student, self.thesis.__str__())


@python_2_unicode_compatible
class ContactData(ContactModel):
    first_name = models.CharField(_('First name'), max_length=30, null=True, blank=True)
    last_name = models.CharField(_('Last name'), max_length=30, null=True, blank=True)
    email = models.EmailField(_('Email'), null=True, blank=True)

    def __str__(self):
        if self.first_name and self.last_name:
            return u"{} {} {}".format(self.title if self.title else '', self.first_name, self.last_name)
        else:
            return ''


class PlacementCompanyContactData(ContactData):
    placement = models.OneToOneField(Placement, null=True)

    class Meta:
        verbose_name = _('Placement company contact')
        verbose_name_plural = _('Placement company contacts')

    def __str__(self):
        return self.placement.student.__str__()


class Comment(models.Model):
    author = models.ForeignKey(MentoringUser)
    abstractwork = models.ForeignKey(AbstractWork, verbose_name="{}/{}".format(_('Placement'), _('Thesis')))
    message = models.TextField(_('message'))
    timestamp = models.DateTimeField(_('timestamp'), auto_now_add=True)
    private = models.BooleanField(_('Only visible for me'), default=False)

    def __str__(self):
        return self.author.__str__() + " " + date(localtime(self.timestamp), 'SHORT_DATETIME_FORMAT')

    class Meta:
        verbose_name = _('Comment')
        verbose_name_plural = _('Comments')
