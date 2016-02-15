from autofixture import AutoFixture
from django.db.models.signals import *
from django.dispatch import receiver

from mentoring.models import *

__author__ = 'ullmanfa'


@receiver(post_save, sender=Placement)
def post_save_placement(sender, instance, created, **kwargs):
    if created:
        print("post_save_placement")
        ccd = AutoFixture(PlacementCompanyContactData, field_values={'placement': instance}, overwrite_defaults=True)
        ccd.create(1)
        sap = AutoFixture(StudentActivePlacement, field_values={'student': instance.student, 'placement': instance})
        sap.create(1)


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
