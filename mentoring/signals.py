from django.db.models.signals import *
from django.dispatch import receiver

from mentoring.models import *

__author__ = 'ullmanfa'

global delete_user


@receiver(post_save, sender=MentoringUser)
def create_user_profile(sender, instance, created, **kwargs):
    if not instance.gidNumber:
        return

    if int(instance.gidNumber) == 1200:
        extended_user = Student.objects.get_or_create(user=instance)[0]
        extended_user.save()
    elif int(instance.gidNumber) == 1000:
        extended_user = Tutor.objects.get_or_create(user=instance)[0]
        extended_user.save()
    else:
        pass


@receiver(pre_delete, sender=MentoringUser)
def pre_delete_user_profile(sender, instance, using, **kwargs):
    global delete_user
    delete_user = True


@receiver(post_delete, sender=MentoringUser)
def post_delete_user_profile(sender, instance, using, **kwargs):
    print('post_delete_user_profile')


@receiver(post_save, sender=Placement)
def post_save_placement(sender, instance, created, **kwargs):
    if created:
        print("post_save_placement")
        PlacementCompanyContactData.objects.get_or_create(placement=instance)
        sap = StudentActivePlacement.objects.get_or_create(student=instance.student)[0]
        sap.placement = instance
        sap.save()


@receiver(post_save, sender=Thesis)
def post_save_thesis(sender, instance, created, **kwargs):
    if created:
        print("post_save_thesis")
        sap = StudentActiveThesis.objects.get_or_create(student=instance.student)[0]
        sap.thesis = instance
        sap.save()


@receiver(post_save, sender=Student)
def post_save_student(sender, instance, created, **kwargs):
    if created:
        Placement.objects.get_or_create(student=instance)
        Thesis.objects.get_or_create(student=instance)
