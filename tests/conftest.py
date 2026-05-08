import pytest
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from services.constants import Role

User = get_user_model()


@pytest.fixture
def api_client():
    """
    Unauthenticated API client.
    """
    return APIClient()


@pytest.fixture
def patient_user():
    return User.objects.create_user(
        username="patient_user",
        email="patient@example.com",
        password="testpass123",
        role=Role.PATIENT,
    )


@pytest.fixture
def doctor_user():
    return User.objects.create_user(
        username="doctor_user",
        email="doctor@example.com",
        password="testpass123",
        role=Role.DOCTOR,
    )


@pytest.fixture
def nurse_user():
    return User.objects.create_user(
        username="nurse_user",
        email="nurse@example.com",
        password="testpass123",
        role=Role.NURSE,
    )


@pytest.fixture
def staff_user():
    return User.objects.create_user(
        username="staff_user",
        email="staff@example.com",
        password="testpass123",
        role=Role.STAFF,
    )


@pytest.fixture
def patient_client(patient_user):
    client = APIClient()
    client.force_authenticate(user=patient_user)
    return client


@pytest.fixture
def doctor_client(doctor_user):
    client = APIClient()
    client.force_authenticate(user=doctor_user)
    return client


@pytest.fixture
def nurse_client(nurse_user):
    client = APIClient()
    client.force_authenticate(user=nurse_user)
    return client


@pytest.fixture
def staff_client(staff_user):
    client = APIClient()
    client.force_authenticate(user=staff_user)
    return client