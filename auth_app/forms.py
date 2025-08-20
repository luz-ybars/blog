from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.conf import settings


class RegistroForm(UserCreationForm):
    invite_code = forms.CharField(required=False, label='Código de invitación')

    def clean_invite_code(self):
        code = self.cleaned_data.get('invite_code', '').strip()
        expected = (getattr(settings, 'COLAB_INVITE_CODE', '') or '').strip()
        if code and code != expected:
            raise forms.ValidationError('Código de invitación inválido.')
        return code


