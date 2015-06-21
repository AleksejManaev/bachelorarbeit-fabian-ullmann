from django.db.models.signals import *
from django.dispatch import receiver
from mentoring.models import *

__author__ = 'ullmanfa'


@receiver(post_save, sender=AbstractWork)
def post_save_abstractwork(sender, instance, created, **kwargs):
    if created:
        WorkCompany.objects.get_or_create(work=instance)
        print("post_save_abstractwork")


@receiver(post_save, sender=WorkCompany)
def post_save_workcompany(sender, instance, created, **kwargs):
    print("post_save_workcompany")
    if created:
        CompanyContactData.objects.get_or_create(work_company=instance)


@receiver(post_save, sender=Thesis)
def post_save_thesis(sender, instance, created, **kwargs):
    print("post_save_thesis")
    if created:
        post_save_abstractwork(sender, instance, created, **kwargs)
        MentoringRequest.objects.get_or_create(thesis=instance)
        sat = StudentActiveThesis.objects.get_or_create(student=instance.student)[0]
        sat.thesis = instance
        sat.save()


@receiver(post_save, sender=MentoringRequest)
def post_save_mentoringrequest(sender, instance, created, **kwargs):
    print("post_save_mentoringrequest")
    if instance.state == 'AC':
        pass
        # Mentoring.objects.get_or_create(thesis=instance.thesis)


@receiver(post_save, sender=Mentoring)
def post_save_mentoring(sender, instance, created, **kwargs):
    print("post_save_mentoring")
    if created:
        Tutor2ContactData.objects.get_or_create(mentoring=instance)
        Registration.objects.get_or_create(mentoring=instance)
        Colloquium.objects.get_or_create(mentoring=instance)
        MentoringReport.objects.get_or_create(mentoring=instance)


@receiver(post_save, sender=Registration)
def post_save_registration(sender, instance, created, **kwargs):
    if instance.finished:
        ResponseExaminationBoard.objects.get_or_create(registration=instance)


@receiver(post_save, sender=Placement)
def post_save_placement(sender, instance, created, **kwargs):
    print("post_save_placement")
    if created:
        post_save_abstractwork(sender, instance, created, **kwargs)
        sap = StudentActivePlacement.objects.get_or_create(student=instance.student)[0]
        sap.placement = instance
        sap.save()
        per = PlacementEventRegistration.objects.get_or_create(placement=instance)[0]
        per.save()


@receiver(post_delete, sender=Placement)
def post_delete_placement(sender, instance, using, **kwargs):
    sap = StudentActivePlacement.objects.get_or_create(student=instance.student)[0]
    sap.placement = instance.student.placement_set.all().exclude(pk=instance.pk).last()
    sap.save()


@receiver(post_save, sender=Student)
def post_save_student(sender, instance, created, **kwargs):
    print("post_save_student")
    if created:
        Placement.objects.get_or_create(student=instance)
        Thesis.objects.get_or_create(student=instance)
