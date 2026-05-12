from django.http import JsonResponse
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from core.serializers import *
from core.service import *
from rest_framework.filters import SearchFilter
from rest_framework.generics import get_object_or_404, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
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
        instance=create_appointment(serializer.validated_data, self.request.user)
        serializer.instance=instance

class AppointmentDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = AppointmentSerializer
    queryset = Appointment.objects.all()
    permission_classes = [IsStaff]

    def perform_update(self, serializer):
        instance=update_appointment(serializer.instance,serializer.validated_data,self.request.user)
        serializer.instance=instance

#lab reports

class LabReportView(generics.ListCreateAPIView):
    serializer_class = LabReportSerializer
    filter_backends = [DjangoFilterBackend,SearchFilter]
    filterset_class = LabReportFilter
    search_fields = ["patient__user__username", "test_name"]

    def get_queryset(self):
        return get_lab_reports(self.request.user)

    def perform_create(self, serializer):
        instance=create_lab_report(serializer.validated_data, self.request.user)
        serializer.instance=instance
class LabReportDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = LabReportSerializer
    queryset = LabReport.objects.all()
    permission_classes = [IsDoctor]

    def perform_update(self, serializer):
        instance=update_lab_report(serializer.instance,serializer.validated_data,self.request.user)
        serializer.instance=instance

#prescriptions
class PrescriptionView(generics.ListCreateAPIView):
    serializer_class = PrescriptionSerializer
    filter_backends = [DjangoFilterBackend,SearchFilter]
    filterset_class = PrescriptionFilter
    search_fields = ["patient__user__username", "medicines", "notes", ]

    def get_queryset(self):
        return get_prescriptions(self.request.user)

    def perform_create(self, serializer):
       instance=create_prescription(serializer.validated_data, self.request.user)
       serializer.instance=instance

class PrescriptionDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = PrescriptionSerializer
    queryset = Prescription.objects.all()
    permission_classes = [IsDoctor]

    def perform_update(self, serializer):
        instance=update_prescription(serializer.instance,serializer.validated_data,self.request.user)
        serializer.instance=instance

#vitals

class VitalView(generics.ListCreateAPIView):
    serializer_class = VitalsSerializer
    queryset = Vitals.objects.all()

    def get_queryset(self):
        return get_vitals(self.request.user)

    def perform_create(self, serializer):
        instance=create_vital(serializer.validated_data, self.request.user)
        serializer.instance=instance

class VitalDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = VitalsSerializer
    queryset = Vitals.objects.all()
    permission_classes = [IsNurse]
    
    def perform_update(self, serializer):
        instance=update_vital(serializer.instance,serializer.validated_data,self.request.user)
        serializer.instance=instance


class AuditHistoryView(RetrieveAPIView):
    permission_classes = [IsAuthenticated]

    def get_object(self):

        return get_audit_object(
            model_name=self.kwargs["model"],
            pk=self.kwargs["pk"],
            user=self.request.user,
        )

    def retrieve(self, request, *args, **kwargs):

        obj = self.get_object()

        history = get_audit_history(obj)

        return Response(history)