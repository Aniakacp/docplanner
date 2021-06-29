import pytest
from django.test import Client
from django.test import TestCase
from django.urls import reverse
from project.models import *
from project.views import *
from faker import Faker
import pytz
faker = Faker("pl_PL")
from docplanner.settings import TIME_ZONE

# CreateProfile
@pytest.mark.django_db
def test_create_profil():
    c = Client()
    response = c.get("/create-profil/")
    assert response.status_code ==200

@pytest.mark.django_db
def test_create_profil_redirect():
    c = Client()
    new_user= {'username': 'new_user', 'password1':'123', 'password2': '123', 'first_name':'Anna', 'last_name':'Bochenek', 'email':'ania.maria.bochenek@gmail.com'}
    profil= { 'user': new_user, 'pesel':12345678910, 'phone':228538011}
    response = c.post("/create-profil/", profil)
    assert response.status_code == 302

# Login
@pytest.mark.django_db
def test_login():
    c = Client()
    response = c.get("/")
    assert response.status_code ==200

@pytest.mark.django_db
def test_login_redirect(user):
    c = Client()
    data= {'username': user.username, 'password': user.password}
    response = c.post("/", data)
    assert response.status_code ==302

# Logout
@pytest.mark.django_db
def test_main_page(user):
    c = Client()
    c.force_login(user)
    response = c.get("/logout/")
    assert response.status_code ==302
    assert response.url('')

# MainPage
@pytest.mark.django_db
def test_main_page(user, appointments, opinions):
    c = Client()
    c.force_login(user)
    response = c.get(reverse('main'))
    assert response.status_code ==200

# UserDetail
@pytest.mark.django_db
def test_user_detail(user):
    c = Client()
    c.force_login(user)
    response = c.get("/user-detail/")
    assert response.status_code ==200

# Update InfoView
@pytest.mark.django_db
def test_update_info(user):
    c = Client()
    c.force_login(user)
    response= c.get("/update-info/")
    assert response.status_code==200
   # assert response.context['object'] == user

@pytest.mark.django_db
def test_update_profil_not_loged(user):   #zwraca 404
    c= Client()
    response= c.get("/update-info/")
    assert response.status_code==302
   # assert response.url.startswith(reverse('login'))

# ChangePassword
@pytest.mark.django_db
def test_change_password(user):
    c = Client()
    c.force_login(user)
    response = c.get("/change-password/")
    assert response.status_code ==200

# AddAppointment
@pytest.mark.django_db
def test_add_appointment(user):
    c = Client()
    all= Appointment.objects.count()
    c.force_login(user)
    response = c.get("/add-appointment/")
    assert response.status_code ==200

# @pytest.mark.django_db
# def test_add_appointment_if_added(user, address, doctor, patient):
#     c = Client()
#     all_before= Appointment.objects.count()
#     c.force_login(user)
#     date = faker.date_time(tzinfo=pytz.timezone(TIME_ZONE))
   # new_appointment= Appointment.objects.create(date=date, patient=patient, doctor=doctor, address=address))
   # response = c.post("/add-appointment/", new_appointment)
   # assert response.status_code ==201
   # assert Appointment.objects.count() == all_before + 1

# AddOpinion
@pytest.mark.django_db
def test_add_opinion(user):
    c = Client()
    c.force_login(user)
    response = c.get("/add-opinion/")
    assert response.status_code ==200

# UpdateAppointment
@pytest.mark.django_db
def test_edit_appointment(user, appointment):
    c = Client()
    c.force_login(user)
    response = c.get(reverse("edit-appointment", args=(appointment.id, )))
    assert response.status_code ==200
    assert response.context['object'] == appointment

@pytest.mark.django_db
def test_edit_appointment_not_logged(appointment):
    c = Client()
    response = c.get(reverse("edit-appointment", args=(appointment.id, )))
    assert response.status_code == 302  # czy przekierowal
    assert response.url.startswith(reverse('login'))

# DeleteAppointment
@pytest.mark.django_db
def test_delete_appointment(user, appointment):
    c = Client()
    c.force_login(user)
    response = c.get(reverse("delete-appointment", args=(appointment.id, )))
    assert response.status_code ==200

@pytest.mark.django_db
def test_post_delete_appointment(user, appointment):
    c = Client()
    c.force_login(user)
    response = c.post(reverse("delete-appointment", args=(appointment.id, )))
    assert response.status_code ==302
    assert Appointment.objects.count() == 0

# Opinions
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

# Appointments
@pytest.mark.django_db
def test_get_all_appointments(user, appointments):
    c = Client()
    c.force_login(user)
    response = c.get(reverse("appointments"))
    assert response.status_code ==200
    assert len(response.context['appointments']) == len(appointments)  #widok przekazuje do szablonu 'appointments'
    assert len(response.context['appointments']) == Appointment.objects.count()
    for item in response.context['appointments']:
        assert item in appointments