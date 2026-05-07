from django.utils.timezone import now
from datetime import timedelta
from django.db.models import Count, Q, OuterRef, Exists
from core.models import *
from notification.models import Notification
from django.core.cache import cache
from core.cache_key import *


def get_doctor_dashboard_data(doctor):
    key = dashboard_doctor(doctor.id)

    cached = cache.get(key)
    if cached:
        return cached

    current_time = now()
    today = current_time.date()
    week_ago = current_time - timedelta(days=7)

    doctor_appointment=Appointment.objects.filter(doctor=doctor)
    doctor_ordered_lab=LabReport.objects.filter(ordered_by=doctor)

    appointment_stats = doctor_appointment.aggregate(
        today_appointments_count=Count(
            "id",
            filter=Q(scheduled_at__date=today)
        ),

        total_patients_seen=Count(
            "patient",
            filter=Q(status=AppointmentChoices.COMPLETED),
            distinct=True
        ),
    )


    pending_lab_reports_count = doctor_ordered_lab.aggregate(
        count=Count("id",
            filter=Q(status=LabReportChoices.PENDING)
        )
    )["count"]


    prescriptions_issued_this_week = Prescription.objects.filter(
        doctor=doctor
    ).aggregate(
        count=Count(
            "id",
            filter=Q(created_at__gte=week_ago)
        )
    )["count"]

    upcoming_appointments = list(
        doctor_appointment.filter(
            scheduled_at__gte=current_time,
            status=AppointmentChoices.SCHEDULED
        )
        .select_related("patient", "patient__user")
        .order_by("scheduled_at")
        .values(
            "patient__user__username",
            "scheduled_at__date",
            "scheduled_at__time",
            "reason",
        )[:5]
    )

    recent_lab_results = list(
        doctor_ordered_lab.filter(
            status=LabReportChoices.READY)
        .select_related("patient", "patient__user")
        .order_by("-created_at")
        .values(
            "id",
            "status",
            "created_at",
            "patient__user__username",
        )[:5]
    )

    data = {
        "today_appointments_count": appointment_stats["today_appointments_count"] or 0,

        "pending_lab_reports_count": (pending_lab_reports_count or 0),

        "prescriptions_issued_this_week": (prescriptions_issued_this_week or 0),

        "total_patients_seen": appointment_stats["total_patients_seen"] or 0,

        "upcoming_appointments": upcoming_appointments,

        "recent_lab_results": recent_lab_results,
    }

    cache.set(key, data, timeout=120)

    return data


def get_patient_dashboard_data(patient):
    key = dashboard_patient(patient.id)

    cached = cache.get(key)

    if cached:
        return cached

    current_time = now()
    month_ago = current_time - timedelta(days=30)

    user = patient.user

    patient_appointments = Appointment.objects.filter(patient=patient)

    patients_prescriptions = Prescription.objects.filter(patient=patient)


    appointment_stats = patient_appointments.aggregate(
        upcoming_appointments_count=Count(
            "id",
            filter=Q(
                scheduled_at__gte=current_time,
                status=AppointmentChoices.SCHEDULED
            )
        )
    )


    active_prescriptions_count = patients_prescriptions.aggregate(
        count=Count(
            "id",
            filter=Q(created_at__gte=month_ago)
        )
    )["count"]

    pending_lab_reports_count = LabReport.objects.filter(
        patient=patient
    ).aggregate(
        count=Count(
            "id",
            filter=Q(status=LabReportChoices.PENDING)
        )
    )["count"]


    unread_notifications_count = Notification.objects.filter(
        user=user
    ).aggregate(
        count=Count(
            "id",
            filter=Q(is_read=False)
        )
    )["count"]

    next_appointment = (
        patient_appointments.filter(
            scheduled_at__gte=current_time,
            status=AppointmentChoices.SCHEDULED
        )
        .select_related("doctor", "doctor__user")
        .order_by("scheduled_at")
        .values(
            "doctor__user__username",
            "scheduled_at",
            "reason",
        )
        .first()
    )

    latest_vitals = (
        Vitals.objects.filter(
            patient=patient
        )
        .order_by("-recorded_at")
        .values()
        .first()
    )

    recent_prescriptions = list(
        patients_prescriptions
        .order_by("-created_at")
        .values()[:3]
    )

    data = {
        "upcoming_appointments_count": (appointment_stats["upcoming_appointments_count"] or 0),

        "active_prescriptions_count": (active_prescriptions_count or 0),

        "pending_lab_reports_count": (pending_lab_reports_count or 0),

        "unread_notifications_count": (unread_notifications_count or 0),

        "next_appointment": next_appointment,

        "latest_vitals": latest_vitals,

        "recent_prescriptions": recent_prescriptions,
    }

    cache.set(key, data, timeout=120)

    return data


def get_nurse_dashboard_data(nurse):
    key = dashboard_nurse(nurse.id)

    cached = cache.get(key)

    if cached:
        return cached

    current_time = now()
    today = current_time.date()
    week_ago = current_time - timedelta(days=7)


    nurse_vitals = Vitals.objects.filter(recorded_by=nurse)

    vitals_stats = nurse_vitals.aggregate(
        vitals_recorded_today=Count(
            "id",
            filter=Q(created_at__date=today)
        ),

        vitals_recorded_this_week=Count(
            "id",
            filter=Q(created_at__gte=week_ago)
        ),

        distinct_patients_today=Count(
            "patient",
            filter=Q(created_at__date=today),
            distinct=True
        ),
    )

    #checking a patient has a vital today
    vitals_today_subquery = Vitals.objects.filter(
        patient=OuterRef("patient"),
        created_at__date=today
    )

  #scheduled but no vitals til now
    patients_pending_vitals = (
        Appointment.objects.filter(
            scheduled_at__date=today,
            status=AppointmentChoices.SCHEDULED
        )
        .annotate(
            has_vitals=Exists(vitals_today_subquery)
        )
        .filter(
            has_vitals=False
        )
        .aggregate(
            count=Count("patient", distinct=True)
        )["count"]
    )

    recent_vitals = list(
        nurse_vitals
        .select_related(
            "patient",
            "patient__user",
            "recorded_by",
            "recorded_by__user"
        )
        .order_by("-created_at")
        .values(
            "patient__user__username",
            "created_at",
            "recorded_by__user__username",
        )[:5]
    )

    recent_vitals_data = [
        {
            "patient_name": item["patient__user__username"],
            "recorded_at": item["created_at"],
            "recorded_by": item["recorded_by__user__username"],
        }
        for item in recent_vitals
    ]

    data = {
        "vitals_recorded_today": (vitals_stats["vitals_recorded_today"] or 0),

        "vitals_recorded_this_week": (vitals_stats["vitals_recorded_this_week"] or 0),

        "distinct_patients_today": (vitals_stats["distinct_patients_today"] or 0),

        "patients_pending_vitals": (patients_pending_vitals or 0),

        "recent_vitals": recent_vitals_data,
    }

    cache.set(key, data, timeout=120)

    return data