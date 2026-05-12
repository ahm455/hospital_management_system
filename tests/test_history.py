import pytest

from .factories import *

from core.service import update_appointment,create_appointment


# -------------------------
# 1. CREATE HISTORY
# -------------------------
@pytest.mark.django_db
def test_create_history_row():
    obj = AppointmentFactory()

    history = obj.history.all()

    assert history.count() == 1
    assert history.first().history_type == "+"


# -------------------------
# 2. UPDATE HISTORY
# -------------------------
@pytest.mark.django_db
def test_update_history_row():
    obj = AppointmentFactory()

    obj.status = AppointmentChoices.COMPLETED
    obj.save()

    history = obj.history.all()

    assert history.count() == 2
    assert history.first().history_type == "~"


# # -------------------------
# # 3. DELETE HISTORY
# # -------------------------
# @pytest.mark.django_db
# def test_delete_history_row():
#     obj = AppointmentFactory()
#     obj_id = obj.id
#
#     obj.delete()
#
#     history = obj.history.filter(id=obj_id)
#
#     assert history.first().history_type == "-"


# -------------------------
# 4. USER CAPTURE (SERVICE LAYER)
# -------------------------
@pytest.mark.django_db
def test_user_captured_service_layer(staff_user):
    obj = AppointmentFactory(status=AppointmentChoices.SCHEDULED)

    update_appointment(
        obj,
        {"status": AppointmentChoices.CANCELLED},
        user=staff_user
    )

    history = obj.history.first()

    print(f"history:{history.history_type}")
    print(f"history:{history.history_user}")

    assert history.history_user == staff_user


# -------------------------
# 5. AUDIT API RESPONSE SHAPE
# -------------------------

@pytest.mark.django_db
def test_audit_endpoint_shape(staff_client):
    obj = AppointmentFactory()
    print(obj)

    response = staff_client.get(f"/appointments/audit/{obj.id}/")

    assert response.status_code == 200

    data = response.json()[0]

    assert "timestamp" in data
    assert "type" in data
    assert "user" in data
    assert "changed_fields" in data
    assert "state" in data


# -------------------------
# 6. PERMISSION TESTS
# -------------------------
@pytest.mark.django_db
def test_audit_permissions_staff(staff_client,staff_user):
    obj = AppointmentFactory()
    print(obj)
    response = staff_client.get(f"/appointments/audit/{obj.id}/")
    assert response.status_code == 200


@pytest.mark.django_db
def test_audit_permissions_patient(patient_client):
    obj = AppointmentFactory()
    print(obj)
    response = patient_client.get(f"/appointments/audit/{obj.id}/")
    assert response.status_code in [200, 403]


@pytest.mark.django_db
def test_audit_permissions_doctor(doctor_client):
    obj = AppointmentFactory()
    print(obj)
    response = doctor_client.get(f"/appointments/audit/{obj.id}/")
    assert response.status_code in [200, 403]


@pytest.mark.django_db
def test_audit_permissions_anonymous(api_client):
    obj = AppointmentFactory()
    print(obj)
    response = api_client.get(f"/appointments/audit/{obj.id}/")
    assert response.status_code == 401


# -------------------------
# 7. CHANGED FIELDS TEST
# -------------------------
@pytest.mark.django_db
def test_changed_fields_detected():
    obj = AppointmentFactory(status="scheduled")
    print(obj)
    old = obj.status
    obj.status = "completed"
    obj.save()

    history = obj.history.all()

    latest = history[0]
    prev = history[1]

    diff = latest.diff_against(prev)

    assert "status" in diff.changed_fields


