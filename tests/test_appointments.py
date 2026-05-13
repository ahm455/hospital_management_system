import pytest
from core.models import Appointment
from notification.models import Notification
from services.constants import AppointmentChoices
from users.models import Doctor
from .conftest import *
from users.models import *

@pytest.mark.django_db
def test_staff_can_create_appointment(staff_client, patient_user, doctor_user):

    payload = {
        "patient_id": patient_user.patient_profile.id,
        "doctor_id": doctor_user.doctor_profile.id,
        "scheduled_at": "2026-05-13T10:00:00Z",
        "reason": "Fever",
    }

    response = staff_client.post("/appointments/", payload)
    print(response.data)
    assert response.status_code == 201
    assert Appointment.objects.count() == 1


@pytest.mark.django_db
def test_doctor_cannot_create_appointment(doctor_client,doctor_user, patient_user):
    payload = {
        "patient_id": patient_user.patient_profile.id,
        "doctor_id": doctor_user.doctor_profile.id,
        "scheduled_at": "2026-05-13T10:00:00Z",
        "reason": "Checkup",
    }

    response = doctor_client.post("/appointments/", payload)

    assert response.status_code == 403


@pytest.mark.django_db
def test_doctor_sees_only_their_appointments(
    doctor_client,
    doctor_user,
    patient_user,
):
    patient = Patient.objects.get(user=patient_user)
    doctor = Doctor.objects.get(user=doctor_user)

    other_user = User.objects.create_user(
        username="otherdoc",
        password="pass123",
        role=Role.DOCTOR,
    )
    other_doctor = Doctor.objects.get(user=other_user)

    Appointment.objects.create(
        patient_id=patient.id,
        doctor_id=doctor.id,
        reason="Fever",
        scheduled_at="2026-05-13T10:00:00Z",
    )

    Appointment.objects.create(
        patient_id=patient.id,
        doctor_id=other_doctor.id,
        reason="Cold",
        scheduled_at="2026-05-11T10:00:00Z",
    )

    response = doctor_client.get("/appointments/")
    print(response.data)
    assert response.status_code == 200
    assert len(response.data) == 4



@pytest.mark.django_db
def test_search_appointments(staff_client, patient_user, doctor_user):
    patient = Patient.objects.get(user=patient_user)
    doctor = Doctor.objects.get(user=doctor_user)
    Appointment.objects.create(
        patient_id=patient.id,
        doctor_id=doctor.id,
        reason="Fevers",
        scheduled_at="2026-05-10T10:00:00Z",
    )

    Appointment.objects.create(
        patient_id=patient.id,
        doctor_id=doctor.id,
        reason="Headache",
        scheduled_at="2026-05-11T10:00:00Z",
    )

    response = staff_client.get("/appointments/?search=fevers")
    print(response.data)
    assert response.status_code == 200
    assert len(response.data) == 4


@pytest.mark.django_db
def test_cancelling_appointment_does_not_create_booked_notification(
    staff_client,
    patient_user,
    doctor_user,
):
    patient = Patient.objects.get(user=patient_user)
    doctor = Doctor.objects.get(user=doctor_user)
    appointment = Appointment.objects.create(
        patient_id=patient.id,
        doctor_id=doctor.id,
        status=AppointmentChoices.SCHEDULED,
        reason="Checkup",
        scheduled_at="2026-05-10T10:00:00Z",
    )

    response = staff_client.patch(
        f"/appointments/{appointment.id}/",
        {"status": "CANCELLED"},
    )
    print(response.data)
    assert response.status_code == 200

    assert not Notification.objects.filter(
        user=patient_user,
        message__icontains="SCHEDULED"
    ).exists()
