from django.contrib import admin
from django.db.models.loading import get_models, get_app

from .models import AbstractWork, ContactData, ContactModel, PortalUser, Comment


class CommentAdmin(admin.ModelAdmin):
    fields = ('author', 'abstractwork', 'message', 'timestamp', 'private')
    readonly_fields = ('timestamp',)


# Register your models here.
for model in get_models(get_app('mentoring')):
    admin.site.register(model)

admin.site.unregister(AbstractWork)
admin.site.unregister(ContactData)
admin.site.unregister(ContactModel)
admin.site.unregister(PortalUser)
admin.site.unregister(Comment)
admin.site.register(Comment, CommentAdmin)
