import pytest
from core.models import LabReport
from notification.models import Notification
from services.constants import LabReportChoices
from tests.conftest import doctor_client
from users.models import *


@pytest.mark.django_db
def test_ready_lab_report_creates_notification(
    doctor_client,
    patient_user,
    doctor_user,
):
    patient = Patient.objects.get(user=patient_user)
    doctor = Doctor.objects.get(user=doctor_user)
    report = LabReport.objects.create(
        patient=patient,
        status="PENDING",
        ordered_by=doctor,
    )

    payload = {
        "status": "READY"
    }

    response = doctor_client.patch(
        f"/lab-reports/{report.id}/",
        payload,
    )
    print(response.data)
    assert response.status_code == 200

    assert Notification.objects.filter(
        user=patient_user
    ).exists()

@pytest.mark.django_db
def test_filter_pending_lab_reports(
    doctor_client,
    patient_user,
    doctor_user
):
    patient = Patient.objects.get(user=patient_user)
    doctor = Doctor.objects.get(user=doctor_user)

    LabReport.objects.create(
        patient=patient,
        status=LabReportChoices.PENDING,
        ordered_by=doctor,
    )

    LabReport.objects.create(
        patient=patient,
        status=LabReportChoices.READY,
        ordered_by=doctor,
    )

    response = doctor_client.get("/lab-reports/?status=PENDING")

    print(response.data)

    assert response.status_code == 200
    assert response.data["count"] == 1
    assert len(response.data["results"]) == 1