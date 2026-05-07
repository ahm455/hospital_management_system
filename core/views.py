from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from core.serializers import *
from core.service import *
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .permissions import *
from .filter import *

#appointments
class AppointmentView(generics.ListCreateAPIView):
    serializer_class = AppointmentSerializer
    filter_backends = [DjangoFilterBackend,SearchFilter]
    filterset_class = AppointmentFilter
    search_fields = ["patient__user__username","doctor__user__username","reason",]

    def get_queryset(self):
        return get_appointments(self.request.user)


    def perform_create(self, serializer):
        create_appointment(serializer.validated_data, self.request.user)


class AppointmentDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = AppointmentSerializer
    queryset = Appointment.objects.all()
    permission_classes = [IsStaff]

    def perform_update(self, serializer):
        update_appointment(
            serializer.instance,
            serializer.validated_data,
            self.request.user
        )

#lab reports

class LabReportView(generics.ListCreateAPIView):
    serializer_class = LabReportSerializer
    filter_backends = [DjangoFilterBackend,SearchFilter]
    filterset_class = LabReportFilter
    search_fields = ["patient__user__username", "test_name"]

    def get_queryset(self):
        return get_lab_reports(self.request.user)

    def perform_create(self, serializer):
        create_lab_report(serializer.validated_data, self.request.user)

class LabReportDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = LabReportSerializer
    queryset = LabReport.objects.all()
    permission_classes = [IsDoctor]

    def perform_update(self, serializer):
        update_lab_report(
            serializer.instance,
            serializer.validated_data,
            self.request.user
        )


#prescriptions
class PrescriptionView(generics.ListCreateAPIView):
    serializer_class = PrescriptionSerializer
    filter_backends = [DjangoFilterBackend,SearchFilter]
    filterset_class = PrescriptionFilter
    search_fields = ["patient__user__username", "medication", "notes", ]

    def get_queryset(self):
        return get_prescriptions(self.request.user)

    def perform_create(self, serializer):
        create_prescription(serializer.validated_data, self.request.user)


class PrescriptionDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = PrescriptionSerializer
    queryset = Prescription.objects.all()
    permission_classes = [IsDoctor]

    def perform_update(self, serializer):
        update_prescription(
            serializer.instance,
            serializer.validated_data,
            self.request.user
        )

#vitals

class VitalView(generics.ListCreateAPIView):
    serializer_class = VitalsSerializer
    queryset = Vitals.objects.all()

    def get_queryset(self):
        return get_vitals(self.request.user)

    def perform_create(self, serializer):
        create_vital(serializer.validated_data, self.request.user)

class VitalDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = VitalsSerializer
    queryset = Vitals.objects.all()
    permission_classes = [IsNurse]
    
    def perform_update(self, serializer):
        update_vital(
            serializer.instance,
            serializer.validated_data,
            self.request.user
        )