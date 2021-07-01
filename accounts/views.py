from django.contrib.auth import logout, authenticate, login
from django.shortcuts import render, redirect
from django.views import View
from accounts.forms import *
from project.models import *
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from project.permission_mixin import MyTestUserPassesTest

class LoginView(View):
    def get(self, request):
        form=LoginForm()
        return render(request, 'login.html', {'form': form})
    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
            else:
                return render(request, 'login.html', {'form': form, 'message':'Blad logowania!'})
            return redirect('main')
        return render(request, 'login.html', {'form': form})

class LogoutView(MyTestUserPassesTest, View):
    def get(self, request):
        logout(request)
        return redirect('login')

class CreateProfilView(CreateView):
    def get(self, request):
        user_form = CreateUserForm()
        profil_form = CreateProfilForm()
        return render(request, 'profil.html', {'user_form': user_form, 'profil_form':profil_form})

    def post(self, request):
        user_form = CreateUserForm(request.POST)
        profil_form =CreateProfilForm(request.POST)
        if user_form.is_valid() and profil_form.is_valid():
            user = user_form.save(commit=False)
            user.set_password(user_form.cleaned_data['password1'])
            user.save()
            profile = profil_form.save(commit=False)
            profile.user=user
            profile.save()
            return redirect('login')
        return render(request, 'profil.html', {'user_form': user_form, 'profil_form':profil_form})


class ChangePasswordView(MyTestUserPassesTest, View):
    def get(self, request):
        form = ResetPasswordForm()
        return render(request, 'change-password.html', {'form': form})
    def post(self, request):
        form = ResetPasswordForm(request.POST) #nie tworzy obiektu, tylko go updateuje
        if form.is_valid():
            user= request.user
            user.set_password(form.cleaned_data['password1'])
            user.save()
            return redirect('login')
        return render(request, 'change-password.html', {'form': form})

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
            profil_form.save_m2m()   #commit=False bo jest relacja many to many
            return redirect('login')
        return render(request, 'profil.html', {'user_form': user_form, 'profil_form':profil_form})