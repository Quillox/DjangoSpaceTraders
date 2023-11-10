from django import forms

class AcceptContractForm(forms.Form):
    accept = forms.BooleanField(required=False, label='Accept')

class UpdateContractForm(forms.Form):
    update = forms.BooleanField(required=False, label='Update')

