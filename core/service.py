from core.cache_key import *
from datetime import date
from django.core.cache import cache
from rest_framework.exceptions import PermissionDenied, ValidationError
from core.models import *
from core.serializers import *
from core.cache_key import *
from services.constants import *
from notification.service import create_notification

#notification
def appointment_booked(appointment):
    patient_user = appointment.patient.user
    doctor = appointment.doctor

    create_notification(
        user=patient_user,
        title="Appointment Booked",
        message=(
            f"Your appointment has been booked with "
            f"Dr {doctor.user.username} at {appointment.scheduled_at}. "
            f"Please be on time."
        ),
        type="Appointment"
    )


def prescription_issued(prescription):
    patient_user = prescription.patient.user
    doctor = prescription.doctor

    create_notification(
        user=patient_user,
        title="Prescription Issued",
        message=(
            f"Your prescription has been issued by "
            f"Dr {doctor.user.username} for appointment on "
            f"{prescription.appointment.scheduled_at}."
        ),
        type="Prescription"
    )


def lab_report_result_issued(lab_report):
    patient_user = lab_report.patient.user
    doctor = lab_report.ordered_by

    create_notification(
        user=patient_user,
        title="Lab Report Result",
        message=(
            f"Your lab result for {lab_report.test_name} ordered by "
            f"Dr {doctor.user.username} has been issued.\n"
            f"Result: {lab_report.result}"
        ),
        type="LabReport"
    )


#cache
def get_patient_appointments(user):
    key = patient_appts(user.id)

    cached = cache.get(key)
    if cached:
        return cached

    qs = Appointment.objects.filter(patient__user=user).select_related(
        "patient__user",
        "doctor__user"
    )

    data = AppointmentSerializer(qs, many=True).data

    cache.set(key, data, timeout=300)
    return data


def get_doctor_appointments(user):
    today = date.today()
    key = doctor_appts(user.id, today)

    cached = cache.get(key)
    if cached:
        return cached

    qs = Appointment.objects.filter(
        doctor__user=user,
        scheduled_at__date=today
    ).select_related(
        "patient__user",
        "doctor__user"
    )

    data = AppointmentSerializer(qs, many=True).data

    cache.set(key, data, timeout=120)
    return data


def get_patient_prescriptions(user):
    key = patient_prescriptions(user.id)

    cached = cache.get(key)
    if cached:
        return cached

    qs = Prescription.objects.filter(patient__user=user).select_related(
        "patient__user",
        "doctor__user",
        "appointment"
    )

    data = PrescriptionSerializer(qs, many=True).data

    cache.set(key, data, timeout=600)
    return data


def get_patient_labs(user):
    key = patient_labs(user.id)

    cached = cache.get(key)
    if cached:
        return cached

    qs = LabReport.objects.filter(patient__user=user).select_related(
        "patient__user",
        "ordered_by__user"
    )

    data = LabReportSerializer(qs, many=True).data

    cache.set(key, data, timeout=300)
    return data

def get_patient_vitals(user):
    key = patient_vitals(user.id)

    cached = cache.get(key)
    if cached:
        return cached

    qs = Vitals.objects.filter(patient__user=user).select_related(
        "patient__user",
        "recorded_by__user"
    )

    data = VitalsSerializer(qs, many=True).data

    cache.set(key, data, timeout=300)
    return data

#invalid
def invalidate_appointment_cache(appointment):
    cache.delete(patient_appts(appointment.patient.user.id))
    cache.delete(
        doctor_appts(
            appointment.doctor.user.id,
            appointment.scheduled_at.date()
        )
    )


def invalidate_prescription_cache(prescription):
    cache.delete(patient_prescriptions(prescription.patient.user.id))


def invalidate_lab_cache(lab):
    cache.delete(patient_labs(lab.patient.user.id))

def invalidate_vitals_cache(vital):
    cache.delete(patient_vitals(vital.patient.user.id))

# appointment
def create_appointment(data, user):
    if not is_staff(user):
        raise PermissionDenied("Only staff can create appointments")

    appointment = Appointment.objects.create(**data)

    invalidate_appointment_cache(appointment)
    appointment_booked(appointment)

    return appointment


def update_appointment(instance, data, user):
    if not is_staff(user):
        raise PermissionDenied("Only staff can update appointments")

    for k, v in data.items():
        setattr(instance, k, v)

    instance.save()

    invalidate_appointment_cache(instance)
    appointment_booked(instance)

    return instance


def get_appointments(user):
    if is_staff(user):
        return Appointment.objects.all()

    if is_doctor(user):
        return Appointment.objects.filter(doctor__user=user)

    if is_patient(user):
        return Appointment.objects.filter(patient__user=user)

    return Appointment.objects.none()


# lab report
def create_lab_report(data, user):
    if not is_doctor(user):
        raise PermissionDenied("Only doctor can create lab reports")

    lab = LabReport.objects.create(**data)

    invalidate_lab_cache(lab)

    return lab


def update_lab_report(instance, data, user):
    if not is_doctor(user):
        raise PermissionDenied("Only doctor can update lab reports")

    for k, v in data.items():
        setattr(instance, k, v)

    instance.save()

    invalidate_lab_cache(instance)

    if instance.status == LabReportChoices.READY:
        lab_report_result_issued(instance)

    return instance


def get_lab_reports(user):
    if is_doctor(user):
        return LabReport.objects.filter(ordered_by__user=user)

    if is_patient(user):
        return get_patient_labs(user)

    return LabReport.objects.none()


# prescriptions
def create_prescription(data, user):
    if not is_doctor(user):
        raise PermissionDenied("Only doctor can create prescriptions")

    patient = data["patient"]
    doctor = data["doctor"]

    if doctor.user != user:
        raise PermissionDenied("Only doctor can create prescriptions")

    patient_seen = Appointment.objects.filter(doctor=doctor, patient=patient,status=AppointmentChoices.COMPLETED).exists()

    if not patient_seen:
        raise ValidationError("Doctor must have at least one completed appointment with this patient.")


    prescription = Prescription.objects.create(**data)

    invalidate_prescription_cache(prescription)
    prescription_issued(prescription)


    return prescription


def update_prescription(instance, data, user):
    if instance.doctor.user != user:
        raise PermissionDenied("Not allowed")

    for k, v in data.items():
        setattr(instance, k, v)

    instance.save()

    invalidate_prescription_cache(instance)

    return instance


def get_prescriptions(user):
    if is_doctor(user):
        return Prescription.objects.filter(doctor__user=user)

    if is_patient(user):
        return get_patient_prescriptions(user)

    return Prescription.objects.none()


# vitals
def create_vital(data, user):
    if not is_nurse(user):
        raise PermissionDenied("Only nurse can record vitals")

    vital=Vitals.objects.create(**data)
    invalidate_vitals_cache(vital)

    return vital


def update_vital(instance, data, user):
    if instance.recorded_by.user != user:
        raise PermissionDenied("Not allowed")

    for k, v in data.items():
        setattr(instance, k, v)

    instance.save()
    invalidate_vitals_cache(instance)
    return instance


def get_vitals(user):
    if is_doctor(user):
        return Vitals.objects.filter(patient__appointment__doctor__user=user).distinct()

    if is_nurse(user):
        return Vitals.objects.filter(recorded_by__user=user)

    if is_patient(user):
        return get_patient_vitals(user)

    return Vitals.objects.none()