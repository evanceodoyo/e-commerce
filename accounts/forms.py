from dataclasses import field
from pyexpat import model
from django import forms
from .models import Customer

class CustomerAdminForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['name', 'email', 'phone', 'password']