from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from project.models import *
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from doctor.forms import *
from accounts.forms import *

class LoginDoctorView(View):
    def get(self, request):
        form=LoginForm()
        return render(request, 'doctor-login.html', {'form': form})
    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
            else:
                return render(request, 'doctor-login.html', {'form': form, 'message':'Blad logowania!'})
            return redirect('main')
        return render(request, 'doctor-login.html', {'form': form})


class CreateDoctorView(CreateView):
    def get(self, request):
        user_form = CreateUserForm()
        profil_form = CreateDoctorForm()
        return render(request, 'profil.html', {'user_form': user_form, 'profil_form':profil_form})

    def post(self, request):
        user_form = CreateUserForm(request.POST)
        profil_form =CreateDoctorForm(request.POST)
        if user_form.is_valid() and profil_form.is_valid():
            user = user_form.save(commit=False)
            user.set_password(user_form.cleaned_data['password1'])
            user.save()
            profile = profil_form.save(commit=False)
            profile.user=user
            profile.save()
            return redirect('main')
        return render(request, 'doctor-profil.html', {'user_form': user_form, 'profil_form':profil_form})