from django.contrib import admin

from .models import *


# Register your models here.
admin.site.register(AbstractWork)
admin.site.register(Course)
admin.site.register(Placement)
admin.site.register(StudentActivePlacement)
admin.site.register(StudentActiveThesis)
admin.site.register(PortalUser)
admin.site.register(Student)

admin.site.register(Company)
admin.site.register(CompanyContactData)
admin.site.register(ContactData)
admin.site.register(Tutor2ContactData)
admin.site.register(Address)
admin.site.register(Degree)
admin.site.register(WorkCompany)

admin.site.register(Thesis)
admin.site.register(Tutor)

admin.site.register(Mentoring)
admin.site.register(MentoringRequest)
admin.site.register(MentoringUser)
