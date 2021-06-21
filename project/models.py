from django.contrib.auth.models import User
from django.db import models

class Profil(models.Model):
    user= models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    pesel = models.IntegerField()
    phone= models.SmallIntegerField()

class Specialization(models.Model):
    name= models.CharField(max_length= 255)
    description = models.CharField(max_length= 255)

    def __str__(self):
        return self.name

class Doctor(models.Model):
    user= models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    title= models.CharField(max_length=64, blank=True)
    specialization= models.ManyToManyField(Specialization, blank=True)

    def __str__(self):
        return f'{self.title} {self.user.first_name} {self.user.last_name}'

class Clinic(models.Model):
    city = models.CharField(max_length=100)
    street= models.CharField(max_length=255)
    number= models.CharField(max_length=100)

    def __str__(self):
        return f'{self.street} {self.number} {self.city}'

class Appointment(models.Model):
    doctor= models.ForeignKey(Doctor, related_name='doctor', on_delete=models.CASCADE)
    patient= models.ForeignKey(Profil, related_name='patient', on_delete=models.CASCADE)
    date = models.DateTimeField()
    address=  models.OneToOneField(Clinic, on_delete=models.CASCADE)

   # class Meta:
   #     unique_together= ('patient','date')

class Opinions(models.Model):
    doctor= models.ForeignKey(Doctor, related_name='opinion_doctor', on_delete=models.CASCADE)
    patient = models.ForeignKey(Profil, related_name='opinion_patient', on_delete=models.CASCADE)
    opinion = models.TextField(null=True)
