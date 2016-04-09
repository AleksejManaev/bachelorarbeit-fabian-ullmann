# -*- coding: utf-8 -*-

from django.contrib.auth.models import AbstractUser
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _

from mentoring.helpers import *
from mentoring.validators import *

app_label = 'mentoring'

MENTORING_STATE_CHOICES = (
    ('ND', 'not decided'),
    ('MA', 'mentoring accepted'),
    ('MD', 'mentoring denied'),
)

THESIS_CHOICES = (
    ('Bachelor', 'Bachelor'),
    ('Master', 'Master'),
)

GRADE_CHOICES = (
    ('-', '-'),
    ('1,0', '1,0'),
    ('1,3', '1,3'),
    ('1,7', '1,7'),
    ('2,0', '2,0'),
    ('2,3', '2,3'),
    ('3,0', '3,0'),
    ('3,3', '3,3'),
    ('3,7', '3,7'),
    ('4,0', '4,0'),
    ('5,0', '5,0')
)

EXAMINATION_OFFICE_STATE_CHOICES = (
    ('1A', 'not registered'),
    ('1B', 'registration sent'),
    ('2A', 'registration accepted'),
    ('2B', 'registration denied')
)


class MentoringUser(AbstractUser):
    gidNumber = models.IntegerField(null=True)


@python_2_unicode_compatible
class Course(models.Model):
    TIME_CHOICES = (
        ('3', _('3 months')),
        ('6', _('6 months')),
        ('8', _('8 weeks')),
    )
    editing_time = models.CharField(_('editing time thesis'), max_length=1, choices=TIME_CHOICES, default='3')
    description = models.CharField(_('description'), max_length=50)

    def __str__(self):
        return self.description


class ContactModel(models.Model):
    title = models.CharField(_('title'), max_length=30, null=True, blank=True)
    phone = models.CharField(_('phone'), max_length=30, blank=True, null=True)


class PortalUser(ContactModel):
    user = models.OneToOneField(MentoringUser, primary_key=True)


@python_2_unicode_compatible
class Tutor(PortalUser):
    placement_courses = models.ManyToManyField(Course, blank=True, null=True, verbose_name=_('Placement courses'))
    placement_responsible = models.BooleanField(default=False, null=False, blank=False)

    @property
    def get_full_name(self):
        return "%s %s %s" % (self.title, self.user.first_name, self.user.last_name)

    def __str__(self):
        return u"{} {} {}".format(self.title, self.user.first_name, self.user.last_name)


class PlacementSeminar(models.Model):
    placement_year = models.IntegerField(_('Placement year'), blank=True, null=True, unique=True)

    class Meta:
        verbose_name = _('Placement seminar')


class PlacementSeminarEntry(models.Model):
    date = models.DateTimeField()
    placement_seminar = models.ForeignKey(PlacementSeminar)


@python_2_unicode_compatible
class Student(PortalUser):
    matriculation_number = models.CharField(_('Matriculation number'), max_length=8, null=True, blank=True)
    course = models.ForeignKey(Course, verbose_name=_('course placement'), null=True)
    extern_email = models.EmailField(_('extern email address'), null=True, blank=True)
    placement_year = models.IntegerField(_('Placement year'), blank=True, null=True)
    presentation_date = models.ForeignKey(PlacementSeminarEntry, blank=True, null=True, related_name='presentation_student')
    placement_seminar_done = models.BooleanField(_('Placement seminar done'), default=False)
    placement_seminar_entries = models.ManyToManyField(PlacementSeminarEntry, blank=True, related_name='seminar_students')

    def __str__(self):
        return u"{} ({})".format(self.user.get_full_name(), self.matriculation_number)


class Address(models.Model):
    student = models.OneToOneField(Student)
    street = models.CharField(_('street'), max_length=255)
    city = models.CharField(_('city'), max_length=255)
    zip_code = models.CharField(_('zip code'), max_length=30)
    location = models.CharField(_('location'), max_length=100)
    web_address = models.CharField(_('web address'), max_length=255, blank=True, null=True)


class AbstractWork(models.Model):
    student = models.ForeignKey(Student, null=True)
    tutor = models.ForeignKey(Tutor, null=True)
    task = models.TextField(_('task'), null=True)
    created_on = models.DateTimeField(_('date joined'), auto_created=True, auto_now_add=True)
    updated_on = models.DateTimeField(_('date updated'), auto_now=True, null=True)
    sent_on = models.DateTimeField(_('date sent'), blank=True, null=True)
    comment_unread_by_student = models.BooleanField(default=False)
    comment_unread_by_tutor = models.BooleanField(default=False)
    mentoring_requested = models.BooleanField(_('Requested'), default=False)
    mentoring_accepted = models.CharField(max_length=2, choices=MENTORING_STATE_CHOICES, default='ND')

    def __str__(self):
        return "AbstractWork {}".format(self.pk)


@python_2_unicode_compatible
class Placement(AbstractWork):
    company_name = models.CharField(_('company name'), max_length=100, null=True, blank=True)
    company_address = models.TextField(_('company address'), null=True, blank=True)
    date_from = models.DateField(_('internship begin'), blank=True, null=True)
    date_to = models.DateField(_('internship end'), blank=True, null=True)
    report = models.FileField(_('Placement report'), upload_to=upload_to_placement_report, blank=True, null=True, validators=[validate_pdf, validate_size])
    report_uploaded_date = models.DateTimeField(blank=True, null=True)
    certificate = models.FileField(_('Placement certificate'), upload_to=upload_to_placement_certificate, blank=True, null=True, validators=[validate_pdf, validate_size])
    completed = models.BooleanField(_('Completed'), default=False)

    def __str__(self):
        return u"Placement {}".format(self.student.user.username)

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        super(Placement, self).save(force_insert, force_update, using, update_fields)

        # Loeschen alter Upload-Dateien
        # for object in [self.report, self.presentation, self.certificate]:
        #     if (bool(object)):
        #         dir = os.path.dirname(getattr(object, 'path'))
        #         for file in os.listdir(dir):
        #             samefile = os.path.samefile(getattr(object, 'path'), os.path.join(dir, file))
        #             if not samefile:
        #                 os.remove(os.path.join(dir, file))


class StudentActivePlacement(models.Model):
    student = models.OneToOneField(Student)
    placement = models.OneToOneField(Placement, null=True)


class Thesis(AbstractWork):
    type = models.CharField(_('Type'), max_length=100, choices=THESIS_CHOICES, default='Bachelor')
    second_examiner_first_name = models.CharField(_('First name'), max_length=30, null=True, blank=True)
    second_examiner_last_name = models.CharField(_('Last name'), max_length=30, null=True, blank=True)
    second_examiner_organisation = models.CharField(_('Organisation'), max_length=30, null=True, blank=True)
    second_examiner_title = models.CharField(_('title'), max_length=30, null=True, blank=True)
    poster = models.FileField(_('Poster'), upload_to=upload_to_thesis_poster, blank=True, null=True, validators=[validate_pdf, validate_size])
    thesis = models.FileField(_('Thesis'), upload_to=upload_to_thesis_thesis, blank=True, null=True, validators=[validate_pdf, validate_size])
    presentation = models.FileField(_('Presentation'), upload_to=upload_to_thesis_presentation, blank=True, null=True)
    other = models.FileField(_('Other'), upload_to=upload_to_thesis_other, blank=True, null=True)
    grade = models.CharField(_('Grade'), max_length=3, choices=GRADE_CHOICES, default='-')
    examination_office_state = models.CharField(_('Examination office state'), max_length=100, choices=EXAMINATION_OFFICE_STATE_CHOICES, default='1A')
    deadline = models.DateTimeField(_('Deadline'), null=True, blank=True)
    deadline_extended = models.BooleanField(_('Deadline extended'), default=False)
    colloquium_done = models.BooleanField(_('Colloquium done'), default=False)


class StudentActiveThesis(models.Model):
    student = models.OneToOneField(Student)
    thesis = models.OneToOneField(Thesis, null=True)


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


class Comment(models.Model):
    author = models.ForeignKey(MentoringUser)
    abstractwork = models.ForeignKey(AbstractWork)
    message = models.TextField(_('message'))
    timestamp = models.DateTimeField(auto_now_add=True)
    private = models.BooleanField(_('Only visible for me'), default=False)
