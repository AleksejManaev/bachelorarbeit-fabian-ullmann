from django.contrib import admin

from .models import *

# Register your models here.
admin.site.register(AbstractWork)
admin.site.register(Course)
admin.site.register(Placement)
admin.site.register(StudentActivePlacement)
admin.site.register(PortalUser)
admin.site.register(Student)

admin.site.register(PlacementCompanyContactData)
admin.site.register(ContactData)
admin.site.register(Address)

admin.site.register(Tutor)

admin.site.register(MentoringUser)
