from django import forms

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from player.api import SpaceTradersAPI

class TokenForm(forms.Form):
    token = forms.CharField(label='Token', max_length=600)

    def clean_token(self):
        token = self.cleaned_data['token']

        if not SpaceTradersAPI.validate_token(token):
            raise ValidationError(_('Invalid token'))
        return token