from django import forms
from django.contrib.auth.models import User
from project.models import *

class CreateDoctorForm(forms.ModelForm):
    class Meta:
        model = Doctor
        exclude=['user']