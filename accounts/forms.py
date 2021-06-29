from django import forms
from django.contrib.auth.models import User
from project.models import *

class LoginForm(forms.Form):
    username = forms.CharField(max_length=64)
    password= forms.CharField(max_length=64, widget=forms.PasswordInput)

class CreateUserForm(forms.ModelForm):
    password1 = forms.CharField(max_length=64, widget=forms.PasswordInput)
    password2 = forms.CharField(max_length=64, widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'first_name', 'last_name', 'email']

        def clean(self):
            password1 = super().clean().get('password1')
            password2 = super().clean().get('password2')
            email = super().clean().get('email')

            if password1 != password2:
                raise forms.ValidationError('Passwords must be the same')
            elif '@' not in email:
                raise forms.ValidationError('Email doesnt have @')

class CreateProfilForm(forms.ModelForm):
    class Meta:
        model = Profil
        exclude=['user']


class ResetPasswordForm(forms.ModelForm):
    password1= forms.CharField(max_length=64, widget=forms.PasswordInput, label='New password 1')
    password2 = forms.CharField(max_length=64, widget=forms.PasswordInput ,label='New password 2')

    class Meta:
        model= User
        fields=['password1', 'password2']

    def clean(self):
        password1 = super().clean().get('password1')
        password2 = super().clean().get('password2')

        if password1 != password2:
            raise forms.ValidationError('Passwords must be the same')

class CreateDoctorForm(forms.ModelForm):
    class Meta:
        model = Doctor
        exclude=['user']