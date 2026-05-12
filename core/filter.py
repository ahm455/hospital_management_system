import django_filters
from core.models import *
from services import common
from services.common import *


class AppointmentFilter(django_filters.FilterSet):
    status = django_filters.CharFilter(field_name="status")
    doctor = django_filters.NumberFilter(method="filter_doctor")
    patient = django_filters.NumberFilter(method="filter_patient")

    date_from = django_filters.DateFilter(
        field_name="scheduled_at__date",
        lookup_expr="gte"
    )

    date_to = django_filters.DateFilter(
        field_name="scheduled_at__date",
        lookup_expr="lte"
    )

    class Meta:
        model = Appointment
        fields = []

    def filter_doctor(self, queryset, name, value):
        user = self.request.user

        if is_staff(user):
            return queryset.filter(doctor_id=value)

        return queryset

    def filter_patient(self, queryset, name, value):
        user = self.request.user

        if is_staff(user) or is_doctor(user):
            return queryset.filter(patient_id=value)

        return queryset




class PrescriptionFilter(django_filters.FilterSet):

    doctor = django_filters.NumberFilter(method="filter_doctor")

    date_from = django_filters.DateFilter(
        field_name="created_at",
        lookup_expr="gte"
    )

    date_to = django_filters.DateFilter(
        field_name="created_at",
        lookup_expr="lte"
    )

    class Meta:
        model = Prescription
        fields = []

    def filter_doctor(self, queryset, name, value):
        user = self.request.user

        if is_patient(user):
            return queryset.filter(doctor_id=value)

        return queryset




class LabReportFilter(django_filters.FilterSet):

    status = django_filters.CharFilter(field_name="status")

    test_name = django_filters.CharFilter(
        field_name="test_name",
        lookup_expr="exact"
    )

    date_from = django_filters.DateFilter(
        field_name="created_at",
        lookup_expr="gte"
    )

    class Meta:
        model = LabReport
        fields = []