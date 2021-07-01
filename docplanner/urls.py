"""docplanner URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from project.views import *
from accounts.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('create-profil/', CreateProfilView.as_view(), name='create-profil'),
    path('user-detail/', UserDetailView.as_view(), name='user-detail'),
    path('main/', MainPageView.as_view(), name='main'),
    path('change-password/', ChangePasswordView.as_view(), name='change-password'),
    path('update-info/', UpdateInfoView.as_view(), name='update-info'),
    path('add-appointment/', AddAppointmentView.as_view(), name='add-appointment'),
    path('add-opinion/', AddOpinionView.as_view(), name='add-opinion'),
    path('edit-appointment/<int:pk>/', EditAppointmentView.as_view(), name='edit-appointment'),
    path('delete-appointment/<int:pk>/', DeleteAppointmentView.as_view(), name='delete-appointment'),
    path('opinions/', OpinionsView.as_view(), name='opinions'),
    path('doctors/', DoctorsView.as_view(), name='doctors'),
    path('create-doctor/', CreateDoctorView.as_view(), name='create-doctor'),
    path('clinics/', ClinicsView.as_view(), name='clinics'),
#  path('edit-opinion/<int:pk>/', EditOpinionView.as_view(), name='edit-opinion'),
#  path('delete-opinion/<int:pk>/', DeleteOpinionView.as_view(), name='delete-opinion'),
#  path('appointments/', AppointmentsView.as_view(), name='appointments'),
]