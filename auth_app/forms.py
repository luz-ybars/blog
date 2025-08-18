from django import forms
from django.contrib.auth.forms import UserCreationForm


class RegistroForm(UserCreationForm):
    invite_code = forms.CharField(required=False, label='Código de invitación')


