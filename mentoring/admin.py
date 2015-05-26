from django.contrib import admin

from .models import *


# Register your models here.
admin.site.register(AbstractWork)
admin.site.register(Course)
admin.site.register(Placement)
admin.site.register(PortalUser)
admin.site.register(Student)

admin.site.register(Company)
admin.site.register(ContactModel)
admin.site.register(ContactData)
admin.site.register(Address)
admin.site.register(Degree)
admin.site.register(WorkCompany)

admin.site.register(Thesis)
admin.site.register(Tutor)

admin.site.register(Mentoring)
admin.site.register(MentoringRequest)
