# -*- coding: utf-8 -*-
import os

from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

from mentoring.helpers import *
from mentoring.validators import *

class Course(models.Model):
    TIME_CHOICES = (
        ('3', _('3 months')),
        ('6', _('6 months')),
        ('8', _('8 weeks')),
    )
    editing_time = models.CharField(_('editing time thesis'), max_length=1, choices=TIME_CHOICES, default='3')
    description = models.CharField(_('description'), max_length=255)

    def __str__(self):
        return self.description

class Degree(models.Model):
    description = models.CharField(_('description'), max_length=255)

    def __str__(self):
        return self.description

class Company(models.Model):
    name = models.CharField(_('company name'), max_length=100, unique=True)

    def __str__(self):
        return self.name


class ContactModel(models.Model):
    title = models.CharField(_('title'), max_length=30, null=True, blank=True)
    phone = models.CharField(_('phone'), max_length=30, blank=True, null=True)


class PortalUser(ContactModel):
    user = models.OneToOneField(User, primary_key=True)

class Student(PortalUser):
    course = models.ForeignKey(Course)
    matriculation_number = models.CharField(_('matriculation number'), max_length=8)
    extern_email = models.EmailField()

    def __str__(self):
        return "{} ({})".format(self.user.get_full_name(), self.matriculation_number)

class Address(models.Model):
    portal_user = models.OneToOneField(Student)
    street = models.CharField(_('street'), max_length=255)
    city = models.CharField(_('city'), max_length=255)
    zip_code = models.CharField(_('zip code'), max_length=30)
    location = models.CharField(_('location'), max_length=100)
    web_address = models.CharField(_('web address'), max_length=255, blank=True, null=True)

class AbstractWork(models.Model):
    description = models.TextField(_('description'), blank=True, null=True)
    created_on = models.DateTimeField(_('date joined'), auto_created=True, auto_now_add=True)
    updated_on = models.DateTimeField(_('date updated'), auto_now=True, null=True)
    finished = models.BooleanField(_('finished'), default=False)

    def __str__(self):
        return "AbstractWork {}".format(self.pk)

class Placement(AbstractWork):
    student = models.OneToOneField(Student, unique=True)
    report = models.FileField(_('report'), upload_to=upload_to_report, blank=True, null=True,
                              validators=[validate_pdf, validate_size])
    presentation = models.FileField(_('presentation'), upload_to=upload_to_presentation, blank=True, null=True,
                                    validators=[validate_pdf, validate_size])
    certificate = models.FileField(_('certificate'), upload_to=upload_to_certificate, blank=True, null=True,
                                   validators=[validate_pdf, validate_size])
    public = models.BooleanField(_('public'), default=False)

    def __str__(self):
        return "Placement {}".format(self.student.user.username)

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        super(Placement, self).save(force_insert, force_update, using, update_fields)

        # Loeschen alter Upload-Dateien

        for object in [self.report, self.presentation, self.certificate]:
            if (bool(object)):
                dir = os.path.dirname(getattr(object, 'path'))
                for file in os.listdir(dir):
                    samefile = os.path.samefile(getattr(object, 'path'), os.path.join(dir, file))
                    if not samefile:
                        os.remove(os.path.join(dir, file))

class WorkCompany(models.Model):
    work = models.OneToOneField(AbstractWork, primary_key=True)
    company = models.ForeignKey(Company, null=True, blank=True)
    description = models.TextField(_('company description'), blank=False)


class ContactData(ContactModel):
    first_name = models.CharField(_('first name'), max_length=30)
    last_name = models.CharField(_('last name'), max_length=30)
    email = models.EmailField(_('email'))

    def __str__(self):
        return "{} {} {}".format(self.title, self.first_name, self.last_name)

class CompanyContactData(ContactData):
    work_company = models.OneToOneField(WorkCompany)

    def __str__(self):
        return "{} {}".format(self.first_name, self.last_name)

class Thesis(AbstractWork):
    student = models.OneToOneField(Student, unique=True)

    def __str__(self):
        return ('Thesis {}'.format(self.student.user.username))

    @property
    def mentoring(self):
        return self.mentoringrequest.mentoring

    @property
    def registration(self):
        if hasattr(self.mentoringrequest, 'mentoring'):
            return self.mentoringrequest.mentoring.registration
        else:
            return None

class Tutor(PortalUser):
    @property
    def requests(self):
        return MentoringRequest.objects.filter(tutor_email=self.user.email, status='RE')

    @property
    def mentorings(self):
        return Mentoring.objects.filter(tutor_1=self)

    def __str__(self):
        return "{} {} {}".format(self.title, self.user.first_name, self.user.last_name)

class MentoringRequest(models.Model):
    STATUS_CHOICES = (
        ('NR', 'not requested'),
        ('RE', 'requested'),
        ('AC', 'accepted'),
        ('DE', 'denied'),
    )
    thesis = models.OneToOneField(Thesis)
    tutor_email = models.EmailField(_('Tutor email'), blank=True, null=True)
    requested_on = models.DateTimeField(_('requested on'), null=True, editable=False)
    status = models.CharField(max_length=2, choices=STATUS_CHOICES, default='NR')
    comment = models.TextField(_('comment'), blank=True, null=True)
    answer = models.TextField(_('answer'), blank=True, null=True)

    def __str__(self):
        return "Request for {}".format(self.tutor_email)

    def from_student(self):
        return self.thesis.student

class Mentoring(models.Model):
    request = models.OneToOneField(MentoringRequest)
    tutor_1 = models.ForeignKey(Tutor)
    created_on = models.DateTimeField(auto_created=True, auto_now_add=True)

    @property
    def thesis(self):
        return self.request.thesis

    @property
    def tutor_2(self):
        return self.tutor2contactdata


class Tutor2ContactData(models.Model):
    mentoring = models.OneToOneField(Mentoring)
    contact = models.OneToOneField(ContactData)

    def __str__(self):
        return "{} {} {}".format(self.contact.title, self.contact.first_name, self.contact.last_name)
class MentoringReport(models.Model):
    mentoring = models.OneToOneField(Mentoring)
    date_initial_meeting = models.DateField(_('date initial meeting'), null=True, blank=True)
    date_deadline = models.DateField(_('date deadline'), null=True, blank=True)

class MentoringReportItem(models.Model):
    report = models.OneToOneField(MentoringReport)
    subject = models.CharField(_('subject'), max_length=100)
    message = models.TextField(_('message'), null=True, blank=True)
    created_on = models.DateTimeField(auto_created=True, auto_now_add=True)

class Registration(models.Model):
    mentoring = models.OneToOneField(Mentoring)
    subject = models.TextField(_('subject'), max_length=250, default='')
    date = models.DateField(_('date'), auto_now=True)
    permission_contact = models.BooleanField(_('permission contact'), default=False)
    permission_infocus = models.BooleanField(_('permission INFOCUS'), default=False)
    permission_public = models.BooleanField(_('permission public'), default=False)
    permission_library = models.BooleanField(_('permission library'), default=False)
    permission_library_tutor = models.BooleanField(_('permission library tutor'), default=False)

    def student(self):
        return self.mentoring.request.from_student()

class ResponseExaminationBoard(models.Model):
    registration = models.OneToOneField(Registration)
    start_editing = models.DateField(_('start editing'))
    stop_editing = models.DateField(_('stop editing'))
    extend_to = models.DateField(_('extended to'))
    delivery = models.DateField(_('delivery thesis'))

class Colloquium(models.Model):
    mentoring = models.OneToOneField(Mentoring)
    date_colloquium = models.DateTimeField(_('date colloquium'))

class CompanyRating(models.Model):
    rate = models.PositiveSmallIntegerField(_('rate'))
    thesis = models.ForeignKey(Thesis)
    comment = models.TextField(_('comment'))
    public = models.BooleanField(default=False)


@receiver(post_save, sender=MentoringRequest)
def post_save_mentoring(sender, instance, created, **kwargs):
    print "post_save_mentoringrequest"
    if instance.status == 'AC':
        print(instance.status)


@receiver(post_save, sender=Student)
def post_save_student(sender, instance, created, **kwargs):
    if created:
        placement = Placement.objects.get_or_create(student=instance)[0]
        thesis = Thesis.objects.get_or_create(student=instance)[0]

        CompanyContactData.objects.get_or_create(
            work_company=WorkCompany.objects.get_or_create(
                work=placement)[0])
        CompanyContactData.objects.get_or_create(
            work_company=WorkCompany.objects.get_or_create(
                work=thesis)[0])
        mr = MentoringRequest(status='NR')
        mr.thesis = thesis
        mr.save()
        # Mentoring.objects.get_or_create(thesis=thesis, tutor_1=mr)
        Address.objects.get_or_create(portal_user=instance)


@receiver(post_delete, sender=CompanyContactData)
def post_delete_contactdata(sender, instance, using, **kwargs):
    CompanyContactData.objects.get_or_create(work_company=instance.work_company)
