from django.db import models

class Role(models.TextChoices):
    PATIENT = "PATIENT", "Patient"
    DOCTOR = "DOCTOR", "Doctor"
    NURSE = "NURSE", "Nurse"
    STAFF = "STAFF", "Staff"

class AppointmentChoices(models.TextChoices):
    SCHEDULED = "SCHEDULED", "Scheduled"
    COMPLETED = "COMPLETED", "Completed"
    CANCELLED = "CANCELLED", "Cancelled"

class LabReportChoices(models.TextChoices):
    PENDING = "PENDING", "Pending"
    READY = "READY", "Ready"

class Gender(models.TextChoices):
    MALE = "MALE", "Male"
    FEMALE = "FEMALE", "Female"

class NotificationType(models.TextChoices):
    APPOINTMENT = "Appointment"
    PRESCRIPTION = "Prescription"
    LAB_REPORT = "LabReport"