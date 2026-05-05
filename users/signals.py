from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import User, Patient, Doctor, Nurse, Staff
from services.constants import Role


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if not created:
        return
    if instance.role == Role.PATIENT:
        Patient.objects.get_or_create(user=instance)

    elif instance.role == Role.DOCTOR:
        Doctor.objects.get_or_create(user=instance)

    elif instance.role == Role.NURSE:
        Nurse.objects.get_or_create(user=instance)

    elif instance.role == Role.STAFF:
        Staff.objects.get_or_create(user=instance)