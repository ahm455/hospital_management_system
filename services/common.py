from django.db import models
from .constants import Role

class TimeStamp(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


def is_staff(user):
    return user.role == Role.STAFF


def is_doctor(user):
    return user.role == Role.DOCTOR


def is_patient(user):
    return user.role == Role.PATIENT


def is_nurse(user):
    return user.role == Role.NURSE