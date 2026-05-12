from datetime import date
from core.models import Appointment
from django.core.cache import cache
from rest_framework.exceptions import PermissionDenied, ValidationError
from core.models import *
from core.serializers import *
from core.cache_key import *
from rest_framework.generics import get_object_or_404
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

    # data = AppointmentSerializer(qs, many=True).data

    cache.set(key, qs, timeout=300)

    return qs


def get_doctor_appointments(user):
    today = date.today()
    key = doctor_appts(user.id, today)

    cached = cache.get(key)
    if cached:
        print("cache hit")
        return cached

    qs = Appointment.objects.filter(
        doctor__user=user,
        scheduled_at__date=today
    ).select_related(
        "patient__user",
        "doctor__user"
    )

    data = AppointmentSerializer(qs, many=True).data

    cache.set(key, qs, timeout=120)
    return qs


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

    cache.set(key, qs, timeout=600)
    return qs


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

    cache.set(key, qs, timeout=300)
    return qs

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

    cache.set(key, qs, timeout=300)
    return qs

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

def invalidate_patient_dashboard_cache(patient):
    cache.delete(dashboard_patient(patient.id))

def invalidate_doctor_dashboard_cache(doctor):
    cache.delete(dashboard_doctor(doctor.id))

def invalidate_nurse_dashboard_cache(nurse):
    cache.delete(dashboard_nurse(nurse.id))


# appointment
def create_appointment(data, user):
    if not is_staff(user):
        raise PermissionDenied("Only staff can create appointments")

    appointment = Appointment.objects.create(**data)

    patient=appointment.patient
    doctor=appointment.doctor

    invalidate_appointment_cache(appointment)
    invalidate_patient_dashboard_cache(patient)
    invalidate_doctor_dashboard_cache(doctor)
    appointment_booked(appointment)

    return appointment


def update_appointment(instance, data, user):
    if not is_staff(user):
        raise PermissionDenied("Only staff can update appointments")

    patient=instance.patient
    doctor=instance.doctor

    for k, v in data.items():
        setattr(instance, k, v)

    instance._history_user = user

    instance.save()

    invalidate_appointment_cache(instance)
    invalidate_patient_dashboard_cache(patient)
    invalidate_doctor_dashboard_cache(doctor)

    return instance


def get_appointments(user):
    if is_staff(user):
        return Appointment.objects.all()

    if is_doctor(user):
        return get_doctor_appointments(user)

    if is_patient(user):
        return get_patient_appointments(user)

    return Appointment.objects.none()


# lab report
def create_lab_report(data, user):
    if not is_doctor(user):
        raise PermissionDenied("Only doctor can create lab reports")

    lab = LabReport.objects.create(**data)

    patient = lab.patient
    doctor = lab.ordered_by

    invalidate_patient_dashboard_cache(patient)
    invalidate_doctor_dashboard_cache(doctor)

    invalidate_lab_cache(lab)

    return lab


def update_lab_report(instance, data, user):
    if not is_doctor(user):
        raise PermissionDenied("Only doctor can update lab reports")

    for k, v in data.items():
        setattr(instance, k, v)

    instance.save()

    instance._history_user = user
    patient = instance.patient
    doctor = instance.ordered_by

    invalidate_patient_dashboard_cache(patient)
    invalidate_doctor_dashboard_cache(doctor)
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
    appointment=data["appointment"]

    if doctor.user != user or patient != appointment.patient:
        raise PermissionDenied("Doctor and patient don't match the appointment")


    patient_seen = Appointment.objects.filter(doctor=doctor, patient=patient,status=AppointmentChoices.COMPLETED).exists()

    if not patient_seen:
        raise ValidationError("Doctor must have at least one completed appointment with this patient.")


    prescription = Prescription.objects.create(**data)

    invalidate_patient_dashboard_cache(patient)
    invalidate_doctor_dashboard_cache(doctor)
    invalidate_prescription_cache(prescription)
    prescription_issued(prescription)


    return prescription


def update_prescription(instance, data, user):
    if instance.doctor.user != user:
        raise PermissionDenied("Not allowed")

    patient = instance.patient
    doctor = instance.doctor

    for k, v in data.items():
        setattr(instance, k, v)

    instance._history_user = user

    instance.save()

    invalidate_patient_dashboard_cache(patient)
    invalidate_doctor_dashboard_cache(doctor)
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

    nurse = vital.recorded_by
    patient = vital.patient

    invalidate_vitals_cache(vital)
    invalidate_nurse_dashboard_cache(nurse)
    invalidate_patient_dashboard_cache(patient)

    return vital


def update_vital(instance, data, user):
    if instance.recorded_by.user != user:
        raise PermissionDenied("Not allowed")

    nurse=instance.recorded_by
    patient = instance.patient
    instance._history_user = user
    for k, v in data.items():
        setattr(instance, k, v)

    instance.save()
    invalidate_vitals_cache(instance)
    invalidate_nurse_dashboard_cache(nurse)
    invalidate_patient_dashboard_cache(patient)
    return instance


def get_vitals(user):
    if is_doctor(user):
        return Vitals.objects.filter(patient__appointment__doctor__user=user).distinct()

    if is_nurse(user):
        return Vitals.objects.filter(recorded_by__user=user)

    if is_patient(user):
        return get_patient_vitals(user)

    return Vitals.objects.none()

#history

MODEL_MAP = {
    "appointment": Appointment,
    "prescription": Prescription,
    "lab_report": LabReport,
    "vital": Vitals,
}

def get_audit_object(model_name, pk, user):

    model = MODEL_MAP.get(model_name)

    if not model:
        raise PermissionDenied("Unknown audit model")

    obj = get_object_or_404(model, pk=pk)

    if is_staff(user):

        if model.__name__ == "Appointment":
            return obj

        raise PermissionDenied("Not allowed")


    if is_doctor(user):

        # Prescription / Appointment
        if hasattr(obj, "doctor"):
            if obj.doctor.user != user:
                raise PermissionDenied("Not allowed")

        # LabReport
        if hasattr(obj, "ordered_by"):
            if obj.ordered_by.user != user:
                raise PermissionDenied("Not allowed")

        return obj


    if is_nurse(user):

        if model.__name__ != "Vitals":
            raise PermissionDenied("Not allowed")

        if obj.recorded_by.user != user:
            raise PermissionDenied("Not allowed")

        return obj


    if is_patient(user):

        if hasattr(obj, "patient"):
            if obj.patient.user != user:
                raise PermissionDenied("Not allowed")

        return obj

    raise PermissionDenied("Not allowed")

def get_audit_history(obj):

    history_qs = obj.history.all()

    return serialize_history(history_qs)


def safe_value(value):
    if value is None:
        return None

    if hasattr(value, "pk") and hasattr(value, "__class__") and not isinstance(value, (str, int, float, bool)):
        return {
            "id": value.pk,
            "username": value.user.username,
        }

    return value

def serialize_history(history):
    data = []

    history = history.order_by("-history_date")
    history_list = list(history)

    for i, h in enumerate(history_list):
        prev = history_list[i + 1] if i + 1 < len(history_list) else None

        if prev:
            diff = h.diff_against(prev)
            changed_fields = diff.changed_fields
        else:
            changed_fields = []

        data.append({
            "timestamp": h.history_date,
            "type": h.history_type,
            "user": (
                {
                    "id": h.history_user.id,
                    "username": h.history_user.username
                } if h.history_user else None
            ),
            "changed_fields": changed_fields,
            "state": {
                field.name: safe_value(getattr(h, field.name))
                for field in h.instance._meta.fields
                if not field.name.startswith("history_")
                        }
             })

    return data
