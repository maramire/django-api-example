from django.contrib import admin
from . import models
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

# Register your models here.

# Here we define an 'inline' profile form
# that will be attached to user form


class ProfileInline(admin.StackedInline):
    model = models.Profile
    can_delete = False
    verbose_name_plural = 'profile'
    exclude = ('following',)

# Here we explicity attach the profile inline form


class UserAdmin(BaseUserAdmin):
    inlines = (ProfileInline,)


# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)

# Register other models
admin.site.register(models.Profile)
admin.site.register(models.Comment)
admin.site.register(models.Post)
