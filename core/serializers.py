from django.utils.timezone import now
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from .models import *
from users.serializers import *

class AppointmentSerializer(serializers.ModelSerializer):
    doctor = DoctorSerializer(read_only=True)
    patient = PatientSerializer(read_only=True)
    doctor_id = serializers.PrimaryKeyRelatedField(queryset=Doctor.objects.all(),source="doctor",write_only=True)
    patient_id = serializers.PrimaryKeyRelatedField(queryset=Patient.objects.all(),source="patient",write_only=True)

    class Meta:
        model = Appointment
        fields = "__all__"

    def validate(self, data):
        scheduled_at = data.get("scheduled_at")

        if scheduled_at and scheduled_at < now():
            raise ValidationError({"scheduled_at": "Date must be in the future"})

        return data


class MiniAppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields =["scheduled_at","reason","status"]

class LabReportSerializer(serializers.ModelSerializer):
    patient = PatientSerializer(read_only=True)
    ordered_by = DoctorSerializer(read_only=True)
    patient_id = serializers.PrimaryKeyRelatedField(queryset=Patient.objects.all(),source="patient",write_only=True)
    ordered_by_id = serializers.PrimaryKeyRelatedField(queryset=Doctor.objects.all(),source="ordered_by",write_only=True)

    class Meta:
        model = LabReport
        fields = "__all__"

class VitalsSerializer(serializers.ModelSerializer):
    patient = PatientSerializer(read_only=True)
    recorded_by = NurseSerializer(read_only=True)
    patient_id = serializers.PrimaryKeyRelatedField(queryset=Patient.objects.all(),source="patient",write_only=True)
    recorded_by_id = serializers.PrimaryKeyRelatedField(queryset=Nurse.objects.all(),source="recorded_by",write_only=True)

    class Meta:
        model = Vitals
        fields = "__all__"

class PrescriptionSerializer(serializers.ModelSerializer):
    patient = PatientSerializer(read_only=True)
    doctor = DoctorSerializer(read_only=True)
    appointment = MiniAppointmentSerializer(read_only=True)
    patient_id = serializers.PrimaryKeyRelatedField(queryset=Patient.objects.all(),source="patient",write_only=True)
    doctor_id = serializers.PrimaryKeyRelatedField(queryset=Doctor.objects.all(),source="doctor",write_only=True)
    appointment_id = serializers.PrimaryKeyRelatedField(queryset=Appointment.objects.all(),source="appointment",write_only=True)

    class Meta:
        model = Prescription
        fields = "__all__"


