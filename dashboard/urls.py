from django.urls import path
from .views import *



urlpatterns = [
    path("patient/",PatientDashboardView.as_view(),name="patient_dashboard"),
    path("doctor/",DoctorDashboardView.as_view(),name="doctor_dashboard"),
    path("nurse/",NurseDashboardView.as_view(),name="nurse_dashboard"),
]