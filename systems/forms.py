from django import forms

class BooleanForm(forms.Form):
    boolean = forms.BooleanField()
    