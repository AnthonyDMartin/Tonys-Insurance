from django import forms
from django.contrib.auth.models import User
from . import models
from django.forms.widgets import NumberInput


class CustomerUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'password']
        widgets = {
            'password': forms.PasswordInput()
        }


class ExampleForm(forms.Form):
    birth_date = forms.DateField(widget=NumberInput(attrs={'type': 'date'}))


class CustomerForm(forms.ModelForm):
    class Meta:
        model = models.Customer
        fields = ['birth_date', 'address', 'email', 'mobile']
