from django.contrib import admin

# Register your models here.
from django.contrib.auth.admin import UserAdmin

from users import forms
from users.models import ApplicationUser


class ApplicationUserAdminModel(UserAdmin):
    add_form = forms.ApplicationUserCreationFrom
    form = forms.ApplicationUserChangeForm
    model = ApplicationUser
    list_display = ['id', 'username']


admin.site.register(ApplicationUser, ApplicationUserAdminModel)

