from django.urls import path
from .views import *

urlpatterns = [
    # Appointments
    path("appointments/", AppointmentView.as_view(), name="appointment-list"),
    path("appointments/<int:pk>/", AppointmentDetailView.as_view(), name="appointment-detail"),

    # Lab Reports
    path("lab-reports/", LabReportView.as_view(), name="labreport-list"),
    path("lab-reports/<int:pk>/", LabReportDetailView.as_view(), name="labreport-detail"),

    # Prescriptions
    path("prescriptions/", PrescriptionView.as_view(), name="prescription-list"),
    path("prescriptions/<int:pk>/", PrescriptionDetailView.as_view(), name="prescription-detail"),

    # Vitals
    path("vitals/", VitalView.as_view(), name="vital-list"),
    path("vitals/<int:pk>/", VitalDetailView.as_view(), name="vital-detail"),

    #audits
    path("appointments/audit/<int:pk>/", AuditHistoryView.as_view(), {"model": "appointment"}),
    path("prescriptions/audit/<int:pk>/", AuditHistoryView.as_view(), {"model": "prescription"}),
    path("lab-reports/audit/<int:pk>/", AuditHistoryView.as_view(), {"model": "lab_report"}),
    path("vitals/audit/<int:pk>/", AuditHistoryView.as_view(), {"model": "vital"}),
]