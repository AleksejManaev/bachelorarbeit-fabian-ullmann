# -*- coding: utf-8 -*-

from datetime import datetime
from django.utils.encoding import python_2_unicode_compatible
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _
from mentoring.helpers import *
from mentoring.validators import *

app_label = 'mentoring'

STATUS_CHOICES = (
    ('NR', 'not requested'),
    ('RE', 'requested'),
    ('AC', 'accepted'),
    ('DE', 'denied'),
    ('CD', 'canceled'),
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


class Degree(models.Model):
    description = models.CharField(_('description'), max_length=255)

    def __str__(self):
        return self.description


@python_2_unicode_compatible
class Company(models.Model):
    name = models.CharField(_('company name'), max_length=100, null=True, blank=True)

    def __str__(self):
        return self.name

    def works(self):
        return WorkCompany.objects.filter(company=self)


class ContactModel(models.Model):
    title = models.CharField(_('title'), max_length=30, null=True, blank=True)
    phone = models.CharField(_('phone'), max_length=30, blank=True, null=True)


class PortalUser(ContactModel):
    user = models.OneToOneField(MentoringUser, primary_key=True)


@python_2_unicode_compatible
class Tutor(PortalUser):
    placement_courses = models.ManyToManyField(Course, blank=True, null=True)

    @property
    def new_requests(self):
        return MentoringRequest.objects.filter(tutor_email=self.user.email, state='RE').order_by('-requested_on')

    @property
    def requests(self):
        return MentoringRequest.objects.filter(tutor_email=self.user.email).order_by('-requested_on')

    @property
    def get_full_name(self):
        return "%s %s %s" % (self.title, self.user.first_name, self.user.last_name)

    def __str__(self):
        return u"{} {} {}".format(self.title, self.user.first_name, self.user.last_name)


@python_2_unicode_compatible
class Student(PortalUser):
    matriculation_number = models.CharField(_('matriculation number'), max_length=8, null=True, blank=True)
    extern_email = models.EmailField(_('extern email address'), null=True, blank=True)

    def __str__(self):
        return u"{} ({})".format(self.user.get_full_name(), self.matriculation_number)

    @property
    def thesis(self):
        return self.student.studentactivethesis.thesis

    @property
    def placement(self):
        return self.student.studentactiveplacement.placement


class Address(models.Model):
    student = models.OneToOneField(Student)
    street = models.CharField(_('street'), max_length=255)
    city = models.CharField(_('city'), max_length=255)
    zip_code = models.CharField(_('zip code'), max_length=30)
    location = models.CharField(_('location'), max_length=100)
    web_address = models.CharField(_('web address'), max_length=255, blank=True, null=True)


class AbstractWork(models.Model):
    task = models.TextField(_('task'), blank=True, null=True)
    created_on = models.DateTimeField(_('date joined'), auto_created=True, auto_now_add=True)
    updated_on = models.DateTimeField(_('date updated'), auto_now=True, null=True)
    sent_on = models.DateTimeField(_('date sent'), blank=True, null=True)

    state = models.CharField(max_length=2, choices=STATUS_CHOICES, default='NR')

    @property
    def finished(self):
        return bool(self.sent_on) and not self.state == 'NR'

    def __setattr__(self, key, value):
        if not key == 'finished':
            super(AbstractWork, self).__setattr__(key, value)
        elif value == True:
            self.sent_on = datetime.now()
            self.state = 'RE'
        else:
            self.sent_on = None
            self.state = 'NR'

    def __str__(self):
        return "AbstractWork {}".format(self.pk)


class Event(models.Model):
    date = models.DateField(_('date'), null=True, blank=True)
    time = models.TimeField(_('time'), null=True, blank=True)
    room = models.CharField(_('room'), max_length=100, null=True, blank=True)


class PlacementEvent(Event):
    course = models.ForeignKey(Course, verbose_name=_('course placement'))
    tutor = models.ForeignKey(Tutor)

    def __str__(self):
        return "Am %s um %s in %s bei %s" % (self.date, self.time, self.room, self.tutor)


@python_2_unicode_compatible
class Placement(AbstractWork):
    student = models.ForeignKey(Student)
    course = models.ForeignKey(Course, verbose_name=_('course placement'), blank=True, null=True)
    tutor = models.ForeignKey(Tutor, blank=True, null=True)
    date_from = models.DateField(_('internship begin'), blank=True, null=True)
    date_to = models.DateField(_('internship end'), blank=True, null=True)
    report = models.FileField(_('report placement'), upload_to=upload_to_placement_report, blank=True, null=True,
                              validators=[validate_pdf, validate_size])
    presentation = models.FileField(_('presentation placement'), upload_to=upload_to_placement_presentation, blank=True,
                                    null=True,
                                    validators=[validate_pdf, validate_size])
    certificate = models.FileField(_('certificate placement'), upload_to=upload_to_placement_certificate, blank=True,
                                   null=True,
                                   validators=[validate_pdf, validate_size])

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


class PlacementEventRegistration(models.Model):
    placement = models.OneToOneField(Placement)
    event = models.ForeignKey(PlacementEvent, null=True, blank=False)
    confirmed = models.BooleanField(default=False)


class StudentActivePlacement(models.Model):
    student = models.OneToOneField(Student)
    placement = models.OneToOneField(Placement, null=True)


class WorkCompany(models.Model):
    work = models.OneToOneField(AbstractWork, primary_key=True)
    company = models.ForeignKey(Company, null=True, blank=True)
    address = models.TextField(_('company address'), null=True, blank=True)


@python_2_unicode_compatible
class ContactData(ContactModel):
    first_name = models.CharField(_('first name'), max_length=30, null=True, blank=True)
    last_name = models.CharField(_('last name'), max_length=30, null=True, blank=True)
    email = models.EmailField(_('email'), null=True, blank=True)

    def __str__(self):
        return u"{} {} {}".format(self.title, self.first_name, self.last_name)


class CompanyContactData(ContactData):
    work_company = models.OneToOneField(WorkCompany)


@python_2_unicode_compatible
class Thesis(AbstractWork):
    student = models.ForeignKey(Student)
    course = models.ForeignKey(Course, verbose_name=_('course placement'), blank=True, null=True)
    report = models.FileField(_('report thesis'), upload_to=upload_to_thesis_report, blank=True, null=True,
                              validators=[validate_pdf, validate_size])
    poster = models.FileField(_('poster thesis'), upload_to=upload_to_thesis_poster, blank=True, null=True,
                              validators=[validate_pdf, validate_size])
    documents_finished = models.BooleanField(default=False)

    def __str__(self):
        return u'Thesis {}'.format(self.student.user.username)

    @property
    def mentoring(self):
        return self.mentoringrequest.mentoring if hasattr(self.mentoringrequest, 'mentoring') else None

    @property
    def registration(self):
        return Registration.objects.get_or_create(mentoring=self.mentoringrequest.mentoring)[0] if hasattr(
            self.mentoringrequest, 'mentoring') and self.mentoringrequest.mentoring else None


class StudentActiveThesis(models.Model):
    student = models.OneToOneField(Student)
    thesis = models.OneToOneField(Thesis, null=True)


@python_2_unicode_compatible
class MentoringRequest(models.Model):
    thesis = models.OneToOneField(Thesis)
    tutor_email = models.EmailField(_('Tutor email'), blank=True, null=True)
    requested_on = models.DateTimeField(_('requested on'), null=True, editable=False)
    state = models.CharField(max_length=2, choices=STATUS_CHOICES, default='NR')
    comment = models.TextField(_('comment'), blank=True, null=True)
    answer = models.TextField(_('answer'), blank=True, null=True)

    def __str__(self):
        return u"Request for {} from {}".format(self.tutor_email, self.thesis.student)

    def from_student(self):
        return self.thesis.student


class Mentoring(models.Model):
    request = models.OneToOneField(MentoringRequest)
    thesis = models.OneToOneField(Thesis)
    tutor_1 = models.ForeignKey(Tutor)
    created_on = models.DateTimeField(auto_created=True, auto_now_add=True)

    @property
    def tutor_2(self):
        return self.tutor2contactdata


@python_2_unicode_compatible
class Tutor2ContactData(models.Model):
    mentoring = models.OneToOneField(Mentoring)
    contact = models.ForeignKey(ContactData, null=True, blank=True)

    def __str__(self):
        return u"{} {} {}".format(self.contact.title, self.contact.first_name, self.contact.last_name)


class MentoringReport(models.Model):
    mentoring = models.OneToOneField(Mentoring)
    date_initial_meeting = models.DateField(_('date initial meeting'), null=True, blank=True)
    date_deadline = models.DateField(_('date deadline'), null=True, blank=True)

    def items(self):
        return MentoringReportItem.objects.filter(report=self)


class MentoringReportItem(models.Model):
    report = models.ForeignKey(MentoringReport)
    subject = models.CharField(_('subject'), max_length=100)
    message = models.TextField(_('message'), null=True, blank=True)
    created_on = models.DateTimeField(auto_created=True, auto_now_add=True)


class Registration(models.Model):
    mentoring = models.OneToOneField(Mentoring)
    subject = models.TextField(_('subject'), max_length=250, default='')
    date = models.DateField(_('date'), null=True, auto_now=True)
    permission_contact = models.BooleanField(_('permission contact'), default=False)
    permission_infocus = models.BooleanField(_('permission INFOCUS'), default=False)
    permission_public = models.BooleanField(_('permission public'), default=False)
    permission_library = models.BooleanField(_('permission library'), default=False)
    permission_library_tutor = models.BooleanField(_('permission library tutor'), default=False)
    pdf_file = models.TextField(_('PDF File'), null=True, blank=True)
    finished = models.BooleanField(default=False)

    def student(self):
        return self.mentoring.request.from_student()


class ResponseExaminationBoard(models.Model):
    registration = models.OneToOneField(Registration)
    start_editing = models.DateField(_('start editing'), null=True, blank=True)
    stop_editing = models.DateField(_('stop editing'), null=True, blank=True)
    extend_to = models.DateField(_('extended to'), null=True, blank=True)
    finished = models.BooleanField(default=False)


class Colloquium(Event):
    mentoring = models.OneToOneField(Mentoring)


class CompanyRating(models.Model):
    rate = models.PositiveSmallIntegerField(_('rate'))
    thesis = models.ForeignKey(Thesis)
    comment = models.TextField(_('comment'))
    public = models.BooleanField(default=False)
