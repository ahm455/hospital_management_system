from datetime import timedelta
import pytest
from .factories import *

@pytest.mark.django_db
def test_patient_cannot_access_doctor_dashboard(patient_client):
    response = patient_client.get("/dashboard/doctor/")

    assert response.status_code == 403


@pytest.mark.django_db
def test_doctor_dashboard_empty_state(doctor_client):

    response = doctor_client.get("/dashboard/doctor",follow=True)
    print(response.data)

    assert response.status_code == 200

    assert response.data == {'today_appointments_count': 0,
                             'pending_lab_reports_count': 0,
                             'prescriptions_issued_this_week': 0,
                             'total_patients_seen': 0,
                             'upcoming_appointments': [],
                             'recent_lab_results': []}


@pytest.mark.django_db
def test_doctor_dashboard_counts_today_vs_yesterday(doctor_client,doctor_user):

    patient = PatientFactory()

    today = timezone.now()
    yesterday = today - timedelta(days=1)
    doctor = Doctor.objects.get(user=doctor_user)


    AppointmentFactory.create_batch(
        3,
        doctor=doctor,
        patient=patient,
        scheduled_at=today,
        status=AppointmentChoices.SCHEDULED
    )

    AppointmentFactory.create_batch(
        2,
        doctor=doctor,
        patient=patient,
        scheduled_at=yesterday,
        status=AppointmentChoices.SCHEDULED
    )

    response = doctor_client.get("/dashboard/doctor/",follow=True)
    print(response.data)

    assert response.status_code == 200

    data = response.data

    assert data["today_appointments_count"] == 3