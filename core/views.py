from rest_framework import generics
from core.serializers import *
from core.service import *

#appointments
class AppointmentView(generics.ListCreateAPIView):
    serializer_class = AppointmentSerializer

    def get_queryset(self):
        return get_appointments(self.request.user)

    def perform_create(self, serializer):
        create_appointment(serializer.validated_data, self.request.user)

class AppointmentDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = AppointmentSerializer
    queryset = Appointment.objects.all()

    def perform_update(self, serializer):
        update_appointment(
            serializer.instance,
            serializer.validated_data,
            self.request.user
        )

#lab reports

class LabReportView(generics.ListCreateAPIView):
    serializer_class = LabReportSerializer

    def get_queryset(self):
        return get_lab_reports(self.request.user)

    def perform_create(self, serializer):
        create_lab_report(serializer.validated_data, self.request.user)

class LabReportDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = LabReportSerializer
    queryset = LabReport.objects.all()

    def perform_update(self, serializer):
        update_lab_report(
            serializer.instance,
            serializer.validated_data,
            self.request.user
        )


#prescriptions
class PrescriptionView(generics.ListCreateAPIView):
    serializer_class = PrescriptionSerializer

    def get_queryset(self):
        return get_prescriptions(self.request.user)

    def perform_create(self, serializer):
        create_prescription(serializer.validated_data, self.request.user)


class PrescriptionDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = PrescriptionSerializer
    queryset = Prescription.objects.all()

    def perform_update(self, serializer):
        update_prescription(
            serializer.instance,
            serializer.validated_data,
            self.request.user
        )

#vitals

class VitalView(generics.ListCreateAPIView):
    serializer_class = VitalsSerializer

    def get_queryset(self):
        return get_vitals(self.request.user)

    def perform_create(self, serializer):
        create_vital(serializer.validated_data, self.request.user)

class VitalDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = VitalsSerializer
    queryset = Vitals.objects.all()

    def perform_update(self, serializer):
        update_vital(
            serializer.instance,
            serializer.validated_data,
            self.request.user
        )