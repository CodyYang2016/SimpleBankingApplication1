# forms.py
from django import forms
from .models import customer

class customerCreationForm(forms.ModelForm):
    class Meta:
        model = customer
        fields = ['first_name', 'last_name', 'pin']

    pin = forms.CharField(widget=forms.PasswordInput())
