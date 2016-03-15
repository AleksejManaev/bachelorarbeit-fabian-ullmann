# -*- coding: utf-8 -*-

from django.contrib.auth.models import AbstractUser
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _

from mentoring.helpers import *
from mentoring.validators import *

app_label = 'mentoring'

STATUS_CHOICES = (
    ('ND', 'not decided'),
    ('MA', 'mentoring accepted'),
    ('MD', 'mentoring denied'),
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
    placement_courses = models.ManyToManyField(Course, blank=True, null=True)
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
    extern_email = models.EmailField(_('extern email address'), null=True, blank=True)
    placement_year = models.IntegerField(_('Placement year'), blank=True, null=True)
    presentation_date = models.ForeignKey(PlacementSeminarEntry, blank=True, null=True, related_name='presentation_student')
    placement_seminar_done = models.BooleanField(_('Placement seminar done'), default=False)
    placement_seminar_entries = models.ManyToManyField(PlacementSeminarEntry, blank=True, related_name='seminar_students')

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

    # @property
    # def finished(self):
    #     return bool(self.sent_on) and not self.state == 'NR'

    # def __setattr__(self, key, value):
    #     if not key == 'finished':
    #         super(AbstractWork, self).__setattr__(key, value)
    #     elif value == True:
    #         self.sent_on = datetime.now()
    #         self.state = 'RE'
    #     else:
    #         self.sent_on = None
    #         self.state = 'NR'

    def __str__(self):
        return "AbstractWork {}".format(self.pk)


@python_2_unicode_compatible
class Placement(AbstractWork):
    student = models.ForeignKey(Student)
    course = models.ForeignKey(Course, verbose_name=_('course placement'), blank=True, null=True)
    tutor = models.ForeignKey(Tutor, blank=True, null=True)
    company_name = models.CharField(_('company name'), max_length=100, null=True, blank=True)
    company_address = models.TextField(_('company address'), null=True, blank=True)
    date_from = models.DateField(_('internship begin'), blank=True, null=True)
    date_to = models.DateField(_('internship end'), blank=True, null=True)
    report = models.FileField(_('Placement report'), upload_to=upload_to_placement_report, blank=True, null=True,
                              validators=[validate_pdf, validate_size])
    report_uploaded_date = models.DateTimeField(blank=True, null=True)
    certificate = models.FileField(_('Placement certificate'), upload_to=upload_to_placement_certificate,
                                   blank=True,
                                   null=True,
                                   validators=[validate_pdf, validate_size])
    mentoring_requested = models.BooleanField(_('Requested'), default=False)
    mentoring_accepted = models.CharField(max_length=2, choices=STATUS_CHOICES, default='ND')
    placement_completed = models.BooleanField(_('Completed'), default=False)

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


@python_2_unicode_compatible
class ContactData(ContactModel):
    first_name = models.CharField(_('First name'), max_length=30, null=True, blank=True)
    last_name = models.CharField(_('Last name'), max_length=30, null=True, blank=True)
    email = models.EmailField(_('Email'), null=True, blank=True)

    def __str__(self):
        return u"{} {} {}".format(self.title, self.first_name, self.last_name)


class PlacementCompanyContactData(ContactData):
    placement = models.OneToOneField(Placement, null=True)


class Comment(models.Model):
    author = models.ForeignKey(MentoringUser)
    abstract_work = models.ForeignKey(AbstractWork)
    message = models.TextField(_('message'))
    timestamp = models.DateTimeField(auto_now_add=True)
    private = models.BooleanField(_('Only visible for me'), default=False)
