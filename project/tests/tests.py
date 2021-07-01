import pytest
from django.test import Client
from django.test import TestCase
from django.urls import reverse
from project.models import *
from project.views import *
from faker import Faker
import pytz
import datetime
faker = Faker("pl_PL")
from docplanner.settings import TIME_ZONE

@pytest.mark.django_db
def test_create_profil():
    c = Client()
    response = c.get("/create-profil/")
    assert response.status_code ==200

@pytest.mark.django_db
def test_create_doctor():
    c = Client()
    response = c.get("/create-doctor/")
    assert response.status_code ==200

@pytest.mark.django_db
def test_create_profil_redirect():
    c = Client()
    new_user= {'username': 'new_user', 'password1':'123', 'password2': '123', 'first_name':'Anna', 'last_name':'Bochenek', 'email':'ania.maria.bochenek@gmail.com', 'pesel':12345678910, 'phone':228538011}
    response = c.post("/create-profil/", new_user)
    assert response.status_code == 302
    assert response.url.startswith(reverse('login'))

@pytest.mark.django_db
def test_create_doctor_redirect(specializations):
    c = Client()
    new_user= {'username': 'new_user', 'password1':'123', 'password2': '123', 'first_name':'Anna', 'last_name':'Bochenek', 'email':'ania.maria.bochenek@gmail.com', 'title':'ortopeda', 'specialization':specializations}
    response = c.post("/create-profil/", new_user)
    assert response.status_code == 302
    assert response.url.startswith(reverse('login'))

@pytest.mark.django_db
def test_login():
    c = Client()
    response = c.get("/")
    assert response.status_code ==200

@pytest.mark.django_db
def test_login_redirect(user, profil):
    c = Client()
    data= {'username': user.username, 'password': '123'}
    response = c.post("/", data)
    assert response.status_code ==302
    assert response.url.startswith(reverse('login'))

@pytest.mark.django_db
def test_logout_redirect(profil):
    c = Client()
    c.force_login(profil.user)
    response = c.get("/logout/")
    assert response.status_code ==302
    assert response.url.startswith(reverse('login') )

@pytest.mark.django_db
def test_main_page(user, appointments, opinions):
    c = Client()
    c.force_login(user)
    response = c.get(reverse('main'))
    assert response.status_code ==200

@pytest.mark.django_db
def test_user_detail(profil):
    c = Client()
    c.force_login(profil.user)
    response = c.get("/user-detail/")
    assert response.status_code ==200

@pytest.mark.django_db
def test_update_info(profil):
    c = Client()
    c.force_login(profil.user)
    response= c.get("/update-info/")
    assert response.status_code==200
   # assert response.context['object'] == user

@pytest.mark.django_db
def test_update_profil_not_loged(user):
    c= Client()
    response= c.get("/update-info/")
    assert response.status_code == 302
    assert response.url.startswith(reverse('login'))

@pytest.mark.django_db
def test_change_password(profil):
    c = Client()
    c.force_login(profil.user)
    response = c.get("/change-password/")
    assert response.status_code ==200

@pytest.mark.django_db
def test_add_appointment(profil):
    c = Client()
    c.force_login(profil.user)
    response = c.get("/add-appointment/")
    assert response.status_code ==200

@pytest.mark.django_db
def test_add_appointment_redirect(profil, doctor, address):
    c = Client()
    c.force_login(profil.user)
    all_before = Appointment.objects.count()
    data= {'patient': profil, 'doctor': doctor, 'address': address, 'date': datetime.datetime.now()+datetime.timedelta(days=1)}
    response = c.post("/add-appointment/", data)
    assert response.status_code ==302
    assert response.url.startswith(reverse('appointments'))
    assert Appointment.objects.count() == all_before + 1

@pytest.mark.django_db
def test_add_opinion(profil):
    c = Client()
    c.force_login(profil.user)
    response = c.get("/add-opinion/")
    assert response.status_code ==200

@pytest.mark.django_db
def test_edit_appointment(profil, appointment):
    c = Client()
    c.force_login(profil.user)
    response = c.get(reverse("edit-appointment", args=(appointment.id, )))
    assert response.status_code ==200
    assert response.context['object'] == appointment

@pytest.mark.django_db
def test_edit_appointment_not_logged(appointment):
    c = Client()
    response = c.get(reverse("edit-appointment", args=(appointment.id, )))
    assert response.status_code == 302
    assert response.url.startswith(reverse('login'))

@pytest.mark.django_db
def test_delete_appointment(user, appointment):
    c = Client()
    c.force_login(user)
    response = c.get(reverse("delete-appointment", args=(appointment.id, )))
    assert response.status_code ==200

@pytest.mark.django_db
def test_delete_appointment_redirect(profil, appointment):
    c = Client()
    c.force_login(profil.user)
    response = c.post(reverse("delete-appointment", args=(appointment.id, )))
    assert response.status_code ==302
    assert Appointment.objects.count() == 0

@pytest.mark.django_db
def test_get_all_opinions(user, opinions):
    c = Client()
    c.force_login(user)
    response = c.get(reverse("opinions"))
    assert response.status_code ==200
    assert len(response.context['opinions']) == len(opinions)
    assert len(response.context['opinions']) == Opinions.objects.count()
    for item in response.context['opinions']:
        assert item in opinions

@pytest.mark.django_db
def test_get_all_appointments(user, appointments):
    c = Client()
    c.force_login(user)
    response = c.get(reverse("main"))
    assert response.status_code ==200
    assert len(response.context['appointments']) == len(appointments)  #widok przekazuje do szablonu 'appointments'
    assert len(response.context['appointments']) == Appointment.objects.count()
    for item in response.context['appointments']:
        assert item in appointments

@pytest.mark.django_db
def test_get_all_clinics(user, clinics):
    c = Client()
    c.force_login(user)
    response = c.get(reverse("clinics"))
    assert response.status_code ==200
    assert len(response.context['clinics']) == len(clinics)
    assert len(response.context['clinics']) == Clinic.objects.count()
    for item in response.context['clinics']:
        assert item in clinics

@pytest.mark.django_db
def test_get_all_doctors(user, doctors):
    c = Client()
    c.force_login(user)
    response = c.get(reverse("doctors"))
    assert response.status_code ==200
    assert len(response.context['doctors']) == len(doctors)
    assert len(response.context['doctors']) == Doctor.objects.count()
    for item in response.context['doctors']:
        assert item in doctors