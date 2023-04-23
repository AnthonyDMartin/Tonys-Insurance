from django import forms
from django.contrib.auth.models import User
from . import models
from django.forms.widgets import NumberInput


class ExampleForm(forms.Form):
    birth_date = forms.DateField(widget=NumberInput(attrs={'type': 'date'}))


class CustomerUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'password']
        widgets = {
            'password': forms.PasswordInput()
        }


class CustomerForm(forms.ModelForm):
    class Meta:
        model = models.Customer
        fields = ['birth_date', 'address', 'email', 'mobile']


class ContactusForm(forms.Form):
    Jméno = forms.CharField(max_length=30)
    Email = forms.EmailField()
    Zpráva = forms.CharField(max_length=500, widget=forms.Textarea(attrs={'rows': 3, 'cols': 30}))


class CategoryForm(forms.ModelForm):
    class Meta:
        model = models.Category
        fields = ['category_name']


class PolicyForm(forms.ModelForm):
    category = forms.ModelChoiceField(queryset=models.Category.objects.all(), empty_label="Název pojištění",
                                      to_field_name="id")

    class Meta:
        model = models.Policy
        fields = ['policy_name', 'sum_assurance', 'premium', 'tenure']


class QuestionForm(forms.ModelForm):
    class Meta:
        model = models.Question
        fields = ['description']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 6, 'cols': 30})
        }
