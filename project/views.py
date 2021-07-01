from datetime import datetime, timezone
from project.permission_mixin import MyTestUserPassesTest
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from project.models import *
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
import dateutil.parser

class MainPageView(MyTestUserPassesTest, View):
    def get(self, request):
        appointments= Appointment.objects.filter(patient= request.user.profil, date__gte=datetime.now())
        opinions = Opinions.objects.filter(patient=Profil.objects.get(user=request.user))
        username=''
        if request.user.is_authenticated:
            username = request.user.username
        return render(request, 'main.html', {'appointments':appointments, 'opinions':opinions, 'username':username})

class UserDetailView(MyTestUserPassesTest, View):
    def get(self, request):
        return render(request, 'profil-detail.html' )

class UpdateInfoView(MyTestUserPassesTest, UpdateView):
    def get(self, request):
        return render(request, 'update-info.html')
    def post(self, request):
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        user = request.user
        if phone!='':
            Profil.objects.filter(user=user).update(phone=phone)
            return redirect('user-detail')
        if email!='':
            user.email= email
            user.save()
            return redirect('user-detail')
        return render(request, 'update-info.html')


class AddAppointmentView(MyTestUserPassesTest, View):
    def get(self, request):
        doctor= Doctor.objects.all()
        clinic= Clinic.objects.all()
        return render(request, 'add-appointment.html', {'doctor':doctor, 'clinic':clinic })
    def post(self, request):
        doctor= Doctor.objects.get(pk= request.POST.get('doctor'))
        clinic= Clinic.objects.get(pk= request.POST.get('clinic'))
        date = datetime.strptime(request.POST.get('date'), '%Y-%m-%d %H:%M')
        patient= Profil.objects.get(user=request.user)
        if date!='':
            Appointment.objects.create(patient=patient, doctor=doctor, address=clinic, date=date)
            return redirect('appointments')
        return render(request, 'add-appointment.html')

class OpinionsView(MyTestUserPassesTest, View):
    def get(self, request):
        doctors= Doctor.objects.all()
        opinions = Opinions.objects.filter(patient=Profil.objects.get(user=request.user))
        return render(request, 'opinions.html', {'opinions':opinions, 'doctors': doctors })


class AddOpinionView(MyTestUserPassesTest, View):
    def get(self, request):
        doctor= Doctor.objects.all()
        return render(request, 'add-opinion.html', {'doctor':doctor })
    def post(self, request):
        doctor= Doctor.objects.get(pk= request.POST.get('doctor'))
        opinion= request.POST.get('opinion')
        patient = Profil.objects.get(user=request.user)
        if doctor!='' and opinion!='':
            Opinions.objects.create(patient=patient, doctor=doctor, opinion=opinion)
            return redirect('opinions')
        return render(request, 'add-opinion.html')

class EditAppointmentView(MyTestUserPassesTest, UpdateView):
    model = Appointment
    template_name ='edit-appointmemt.html'
    success_url = reverse_lazy('appointments')
    fields=['doctor', 'date', 'address']

class DeleteAppointmentView(MyTestUserPassesTest, DeleteView):
    model = Appointment
    template_name = 'delete-appointment.html'
    success_url = reverse_lazy('appointments')

#class AppointmentsView(MyTestUserPassesTest, View):
#    def get(self, request):
#        appointments= Appointment.objects.filter(patient= request.user.profil, date__gte=datetime.now())
#        return render(request, 'appointments.html', {'appointments':appointments })

#class EditOpinionView(MyTestUserPassesTest, UpdateView):
 #   model = Opinions
#    template_name ='edit-opinion.html'
 #   success_url = reverse_lazy('opinions')
 #   fields=['doctor', 'opinion']

#class DeleteOpinionView(DeleteView):
#    model = Opinions
 #   template_name = 'delete-opinion.html'
 #   success_url = reverse_lazy('opinions')

class DoctorsView(View):
    def get(self, request):
        specializations = Specialization.objects.all()
        doctors= Doctor.objects.all()
        return render(request, 'doctors.html', {'doctors': doctors, 'specializations':specializations })

class ClinicsView(View):
    def get(self, request):
        clinics = Clinic.objects.all()
        return render(request, 'clinics.html', {'clinics': clinics})