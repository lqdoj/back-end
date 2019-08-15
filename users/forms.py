from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User

from users.models import Profile


class UserRegistrationForm(UserCreationForm):
    username = forms.CharField(required=True, min_length=8, max_length=30)

    class Meta:
        model = User
        fields = ("username", "first_name", "last_name", "email", 'password1', 'password2')


class UserUpdateForm(UserChangeForm):
    class Meta:
        model = User
        fields = ("id", "username", "first_name", "last_name", "email")


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ("avatar",)
