from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from users.models import ApplicationUser


class ApplicationUserCreationFrom(UserCreationForm):
    class Meta(UserCreationForm):
        model = ApplicationUser
        fields = '__all__'


class ApplicationUserChangeForm(UserChangeForm):
    class Meta:
        model = ApplicationUser
        fields = '__all__'

