import pytest
from core.models import Appointment
from services.constants import AppointmentChoices
from users.models import Doctor
from .conftest import *
from users.models import *

@pytest.mark.django_db
def test_anonymous_user_cannot_create_appointment(api_client):
    response = api_client.post("/appointments/", {})

    assert response.status_code == 401

@pytest.mark.django_db
def test_staff_can_create_appointment(staff_client, patient_user, doctor_user):

    payload = {
        "patient_id": patient_user.patient_profile.id,
        "doctor_id": doctor_user.doctor_profile.id,
        "scheduled_at": "2026-05-13T10:00:00Z",
        "reason": "Fever",
    }

    response = staff_client.post("/appointments/", payload)

    assert response.status_code == 201
    assert Appointment.objects.count() == 1

@pytest.mark.django_db
def test_doctor_cannot_create_appointment(doctor_client, patient_user, doctor_user):

    payload = {
        "patient_id": patient_user.patient_profile.id,
        "doctor_id": doctor_user.doctor_profile.id,
        "scheduled_at": "2026-05-13T10:00:00Z",
        "reason": "Fever",
    }

    response = doctor_client.post("/appointments/", payload)

    assert response.status_code == 403

@pytest.mark.django_db
def test_patient_can_create_appointment(patient_client, patient_user, doctor_user):

    payload = {
        "patient_id": patient_user.patient_profile.id,
        "doctor_id": doctor_user.doctor_profile.id,
        "scheduled_at": "2026-05-13T10:00:00Z",
        "reason": "Fever",
    }

    response = patient_client.post("/appointments/", payload)

    assert response.status_code == 403



@pytest.mark.django_db
def test_invalid_appointment_data(staff_client):
    payload = {}

    response = staff_client.post("/appointments/", payload)

    assert response.status_code == 400

@pytest.mark.django_db
def test_anonymous_user_cannot_create_appointment(api_client):
    response = api_client.post("/appointments/", {})

    assert response.status_code == 401


@pytest.mark.django_db
def test_invalid_appointment_data(staff_client):
    payload = {}

    response = staff_client.post("/appointments/", payload)

    assert response.status_code == 400

@pytest.mark.django_db
def test_doctor_can_create_prescription(
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
            scheduled_at="2026-05-13T10:00:00Z",
        )

        payload = {
            "patient_id": patient.id,
            "doctor_id": doctor.id,
            "appointment_id": appointment.id,
            "medicines": "Paracetamol",
        }

        response = doctor_client.post("/prescriptions/", payload)
        print(response.data)

        assert response.status_code == 201





