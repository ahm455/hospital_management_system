import pytest
from core.service import create_appointment
from django.utils import timezone
from datetime import timedelta
from services.constants import AppointmentChoices
from tests.factories import DoctorFactory, PatientFactory, AppointmentFactory
from users.models import Doctor

@pytest.mark.django_db
def test_doctor_dashboard_cache_behavior(
    doctor_client,
    doctor_user,
    staff_user,
):

    patient = PatientFactory()
    patient3 = PatientFactory()

    today = timezone.now()

    doctor = Doctor.objects.get(user=doctor_user)

    create_appointment(
        {
            "doctor": doctor,
            "patient": patient,
            "scheduled_at": today,
            "status": AppointmentChoices.SCHEDULED,
        },
        staff_user,
    )

    create_appointment(
        {
            "doctor": doctor,
            "patient": patient3,
            "scheduled_at": today,
            "status": AppointmentChoices.SCHEDULED,
        },
        staff_user,
    )

    response1 = doctor_client.get("/dashboard/doctor/")
    assert response1.data["today_appointments_count"] == 2

    response2 = doctor_client.get("/dashboard/doctor/")
    assert response2.data["today_appointments_count"] == 2

    patient2 = PatientFactory()

    create_appointment(
        {
            "doctor": doctor,
            "patient": patient2,
            "scheduled_at": today,
            "status": AppointmentChoices.SCHEDULED,
        },
        staff_user,
    )

    response3 = doctor_client.get("/dashboard/doctor/")
    assert response3.data["today_appointments_count"] == 3