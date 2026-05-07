from rest_framework.permissions import BasePermission
from services.constants import Role


class IsStaff(BasePermission):
    message = "Only staff can perform this action"

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and
            request.user.role == Role.STAFF
        )


class IsDoctor(BasePermission):
    message = "Only doctors can perform this action"

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and
            request.user.role == Role.DOCTOR
        )


class IsPatient(BasePermission):
    message = "Only patients can perform this action"

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and
            request.user.role == Role.PATIENT
        )


class IsNurse(BasePermission):
    message = "Only nurses can perform this action"

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and
            request.user.role == Role.NURSE
        )