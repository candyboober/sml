from django.contrib.auth.forms import UserCreationForm, UsernameField

from sml_auth.models import User


class RegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("username",)
        field_classes = {'username': UsernameField}
