from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _




class RegisterForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = ('email', 'password1')
        