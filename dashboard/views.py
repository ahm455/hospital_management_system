from core.permissions import *
from django.shortcuts import render
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from .service import *


class DoctorDashboardView(GenericAPIView):
    permission_classes = [IsDoctor]

    def get(self, request, *args, **kwargs):
        user = request.user.doctor_profile
        data = get_doctor_dashboard_data(user)
        return Response(data)

class PatientDashboardView(GenericAPIView):
    permission_classes = [IsPatient]

    def get(self, request, *args, **kwargs):
        user = request.user.patient_profile

        data = get_patient_dashboard_data(user)
        return Response(data)

class NurseDashboardView(GenericAPIView):
    permission_classes = [IsNurse]

    def get(self, request, *args, **kwargs):
        user = request.user.nurse_profile

        data = get_nurse_dashboard_data(user)

        return Response(data)
