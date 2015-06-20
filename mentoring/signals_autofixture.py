from autofixture import AutoFixture
from django.db.models.signals import *
from django.dispatch import receiver
from mentoring.models import *

__author__ = 'ullmanfa'


@receiver(post_save, sender=AbstractWork)
def post_save_abstractwork(sender, instance, created, **kwargs):
    if created:
        print("post_save_abstractwork")
        wc = AutoFixture(WorkCompany, field_values={'work': instance}, overwrite_defaults=True, generate_fk=['company'])
        wc.create(1)


@receiver(post_save, sender=WorkCompany)
def post_save_workcompany(sender, instance, created, **kwargs):
    if created:
        print("post_save_workcompany")
        ccd = AutoFixture(CompanyContactData, field_values={'work_company': instance}, overwrite_defaults=True)
        ccd.create(1)


@receiver(post_save, sender=Thesis)
def post_save_thesis(sender, instance, created, **kwargs):
    if created:
        print("post_save_thesis")
        post_save_abstractwork(sender, instance, created, **kwargs)
        mr = AutoFixture(MentoringRequest, field_values={'thesis': instance}, overwrite_defaults=True)
        mr.create(1)


@receiver(post_save, sender=MentoringRequest)
def post_save_mentoringrequest(sender, instance, created, **kwargs):
    if instance.status == 'AC':
        print("post_save_mentoringrequest")
        m = AutoFixture(Mentoring, field_values={'thesis': instance.thesis}, overwrite_defaults=True)


@receiver(post_save, sender=Mentoring)
def post_save_mentoring(sender, instance, created, **kwargs):
    if created:
        print("post_save_mentoring")
        tcd = AutoFixture(Tutor2ContactData, field_values={'mentoring': instance}, overwrite_defaults=True)
        tcd.create(1)
        r = AutoFixture(Registration, field_values={'mentoring': instance}, overwrite_defaults=True)
        r.create(1)
        c = AutoFixture(Colloquium, field_values={'mentoring': instance}, overwrite_defaults=True)
        c.create(1)
        mr = AutoFixture(MentoringReport, field_values={'mentoring': instance}, overwrite_defaults=True)
        mr.create(1)


@receiver(post_save, sender=Registration)
def post_save_registration(sender, instance, created, **kwargs):
    if instance.finished:
        print("post_save_registration")
        reb = AutoFixture(ResponseExaminationBoard, field_values={'registration': instance}, overwrite_defaults=True)
        reb.create(1)


@receiver(post_save, sender=Placement)
def post_save_placement(sender, instance, created, **kwargs):
    if created:
        print("post_save_placement")
        post_save_abstractwork(sender, instance, created, **kwargs)
        sap = AutoFixture(StudentActivePlacement, field_values={'student': instance.student, 'placement': instance})
        sap.create(1)
        per = AutoFixture(PlacementEventRegistration, field_values={'placement': instance})
        per.create(1)


@receiver(post_save, sender=Student)
def post_save_student(sender, instance, created, **kwargs):
    if created:
        print("post_save_student")
        from autofixture import generators

        pl = AutoFixture(Placement, overwrite_defaults=True,
                         field_values={
                             'report': generators.StaticGenerator('ullmanfa/placement/report/Arbeitszeugnis_Audi.pdf'),
                             'presentation': generators.StaticGenerator(
                                 'ullmanfa/placement/presentation/Arbeitszeugnis_Audi.pdf'),
                             'certificate': generators.StaticGenerator(
                                 'ullmanfa/placement/certificate/Arbeitszeugnis_Audi.pdf'),
                             'student': instance})
        pl.create(1)
        th = AutoFixture(Thesis, overwrite_defaults=True,
                         field_values={
                             'report': generators.StaticGenerator('ullmanfa/placement/report/Arbeitszeugnis_Audi.pdf'),
                             'poster': generators.StaticGenerator(
                                 'ullmanfa/placement/presentation/Arbeitszeugnis_Audi.pdf'),
                             'student': instance})
        th.create(1)
