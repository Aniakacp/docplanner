import datetime

import pytest
from django.contrib.auth.models import User
from project.models import *
from faker import Faker
import pytz
faker = Faker("pl_PL")
#from docplanner.settings import TIME_ZONE

@pytest.fixture
def user():
    u=User()
    u.username ='aniakacp'
    u.set_password('123')
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
def specializations(user):
    s1 = Specialization.objects.create(name='ortopeda', description='lekarz ortopeda')
    s2 = Specialization.objects.create(name='ortopeda', description='lekarz ortopeda')
    return [s1, s2]

@pytest.fixture
def doctor(user2, specializations):
    doctor = Doctor.objects.create(user=user2, title='dr')
    doctor.specialization.set(specializations)
    return doctor

@pytest.fixture
def doctor2(user3, specializations):
    doctor = Doctor.objects.create(user=user3, title='dr mgr')
    doctor.specialization.set(specializations)
    return doctor

@pytest.fixture
def address():
    city='London'
    street='Oxford'
    number='23'
    a =Clinic.objects.create(city=city, street=street, number=number)
    return a

@pytest.fixture
def opinion(profil, doctor):
    doctor = Doctor.objects.create(user= user2)
    opinion ="Cool doctor"
    p =Opinions.objects.create(doctor=doctor, patient=profil, opinion=opinion)
    return p

@pytest.fixture
def opinions(profil, doctor):
    opinion1 = "First opinion"
    opinion2 = "Second opinion"
    opinion1= Opinions.objects.create(doctor=doctor, patient=profil, opinion=opinion1)
    opinion2= Opinions.objects.create(doctor=doctor, patient=profil, opinion=opinion2)
    list=[opinion1, opinion2]
    return list

@pytest.fixture
def clinics():
    clinic1= Clinic.objects.create(city='Warsaw', street="first", number='12')
    clinic2= Clinic.objects.create(city='Warsaw', street="second", number='15')
    list=[clinic1, clinic2]
    return list

@pytest.fixture
def doctors(doctor, doctor2):
    list=[doctor, doctor2]
    return list

@pytest.fixture
def appointment(profil, doctor, address):
    date1 = datetime.datetime.now() + datetime.timedelta(days=1)
    a= Appointment.objects.create(date=date1, patient=profil, doctor=doctor, address=address)
    return a

@pytest.fixture
def appointment2(profil, doctor, address):
    date1 = datetime.datetime.now() + datetime.timedelta(days=2)
    a= Appointment.objects.create(date=date1, patient=profil, doctor=doctor, address=address)
    return a

@pytest.fixture
def appointments(profil, doctor, address, appointment, appointment2):
    list=[appointment, appointment2]
    return list