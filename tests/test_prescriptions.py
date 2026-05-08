import pytest
from core.models import Appointment
from core.models import Prescription
from services.constants import AppointmentChoices
from users.models import *


@pytest.mark.django_db
def test_patient_sees_only_their_prescriptions(
    patient_client,
    patient_user,
    doctor_user,
):
    patient = Patient.objects.get(user=patient_user)
    doctor = Doctor.objects.get(user=doctor_user)
    completed_appointment = Appointment.objects.create(
        patient=patient,
        doctor=doctor,
        status=AppointmentChoices.COMPLETED,
        reason="Fever",
        scheduled_at="2026-05-10T10:00:00Z",
    )

    Prescription.objects.create(
        patient=patient,
        doctor=doctor,
        appointment=completed_appointment,
        medicines="Paracetamol",
    )

    other_patient = patient_user.__class__.objects.create_user(
        username="otherpatient",
        password="pass123",
        role="PATIENT",
    )
    other_patients = Patient.objects.get(user=other_patient)

    other_appointment = Appointment.objects.create(
        patient=other_patients,
        doctor=doctor,
        status=AppointmentChoices.COMPLETED,
        reason="Cold",
        scheduled_at="2026-05-11T10:00:00Z",
    )

    Prescription.objects.create(
        patient=other_patients,
        doctor=doctor,
        appointment=other_appointment,
        medicines="Ibuprofen",
    )

    response = patient_client.get("/prescriptions/")
    print(response.data)

    assert response.status_code == 200
    assert len(response.data) == 4


@pytest.mark.django_db
def test_doctor_cannot_create_prescription_without_completed_appointment(
    doctor_client,
    patient_user,
    doctor_user,
):
    patient = Patient.objects.get(user=patient_user)
    doctor = Doctor.objects.get(user=doctor_user)
    appointment = Appointment.objects.create(
        patient=patient,
        doctor=doctor,
        status=AppointmentChoices.SCHEDULED,
        reason="Checkup",
        scheduled_at="2026-05-10T10:00:00Z",
    )

    payload = {
        "patient": patient.id,
        "appointment": appointment.id,
        "medication": "Paracetamol",
    }

    response = doctor_client.post("/prescriptions/", payload)

    assert response.status_code == 400


@pytest.mark.django_db
def test_doctor_can_create_prescription_with_completed_appointment(
        doctor_client,
        patient_user,
        doctor_user,
):
    patient = Patient.objects.get(user=patient_user)
    doctor = Doctor.objects.get(user=doctor_user)
    appointment = Appointment.objects.create(
        patient=patient,
        doctor=doctor,
        status=AppointmentChoices.COMPLETED,
        reason="Checkup",
        scheduled_at="2026-05-10T10:00:00Z",
    )

    payload = {
        "patient_id": patient.id,
        "doctor_id":doctor.id,
        "appointment_id": appointment.id,
        "medicines": "Paracetamol",
    }

    response = doctor_client.post("/prescriptions/", payload)
    print(response.data)

    assert response.status_code == 201