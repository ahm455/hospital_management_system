
from django.contrib.auth.models import AbstractUser
from django.db import models
from services.constants import Role,Gender
from services.common import TimeStamp


class User(AbstractUser, TimeStamp):
    role = models.CharField(max_length=20, choices=Role.choices)
    date_of_birth = models.DateField(null=True)
    gender = models.CharField(choices=Gender.choices,max_length=10,null=True)
    phone = models.CharField(max_length=20,null=True)

class Patient(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="patient_profile")


class Doctor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="doctor_profile")
    specialization = models.CharField(max_length=100,null=True,blank=True)


class Nurse(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="nurse_profile")


class Staff(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="staff_profile")
