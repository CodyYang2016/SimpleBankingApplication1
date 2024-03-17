# forms.py
from django import forms
from .models import customer

class customerCreationForm(forms.Form):
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)
    email = forms.EmailField(max_length=254)
    raw_password = forms.CharField(label='Password', widget=forms.PasswordInput())


