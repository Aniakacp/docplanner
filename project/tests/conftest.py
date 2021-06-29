import pytest
from django.contrib.auth.models import User
from project.models import *
from faker import Faker
import pytz
faker = Faker("pl_PL")
from docplanner.settings import TIME_ZONE

@pytest.fixture
def user():
    u=User()
    u.username ='aniakacp'
    u.save()
    return u

@pytest.fixture
def user3():
    u=User()
    u.username ='profil'
    u.save()
    return u

@pytest.fixture
def user2():
    u=User()
    u.username ='doctor'
    u.save()
    return u

@pytest.fixture
def profil(user):
    p=Profil()
    p.user = user
    p.pesel=123456789101
    p.phone=228538011
    p.save()
    return p

@pytest.fixture
def doctor(user2):
    doctor = Doctor.objects.create(user=user2)
    return doctor

@pytest.fixture
def patient(user):
    doctor = Profil.objects.create(user=user)
    return doctor

@pytest.fixture
def address():
    city='London'
    street='Oxford'
    number='23'
    a =Clinic.objects.create(city=city, street=street, number=number)
    return a

@pytest.fixture  #bo jest lista wybierana na stronie
def appointment(patient, doctor, address):
    date=faker.date_time(tzinfo=pytz.timezone(TIME_ZONE))
    a= Appointment.objects.create(date=date, patient=patient, doctor=doctor, address=address)
    return a

@pytest.fixture
def opinion(patient, doctor):
    patient = Profil.objects.create(user=user)
    doctor = Doctor.objects.create(user= user2)
    opinion ="Cool doctor"
    p =Opinions.objects.create(doctor=doctor, patient=patient, opinion=opinion)
    return p

@pytest.fixture
def opinions(patient, doctor):
    opinion1 = "First opinion"
    opinion2 = "Second opinion"
    opinion1= Opinions.objects.create(doctor=doctor, patient=patient, opinion=opinion1)
    opinion2= Opinions.objects.create(doctor=doctor, patient=patient, opinion=opinion2)
    list=[opinion1, opinion2]
    return list

@pytest.fixture
def appointments(patient, doctor, address):
    date1 = faker.date_time(tzinfo=pytz.timezone(TIME_ZONE))
    date2 = faker.date_time(tzinfo=pytz.timezone(TIME_ZONE))
    appointment1= Appointment.objects.create(date=date1, patient=patient, doctor=doctor, address=address)
    appointment2= Appointment.objects.create(date=date2, patient=patient, doctor=doctor, address=address)
    list=[appointment1, appointment2]
    return list