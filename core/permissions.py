from rest_framework.permissions import BasePermission


class IsStaff(BasePermission):
    message = "Only staff can perform this action"

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and
            request.user.role == "STAFF"
        )


class IsDoctor(BasePermission):
    message = "Only doctors can perform this action"

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and
            request.user.role == "DOCTOR"
        )


class IsPatient(BasePermission):
    message = "Only patients can perform this action"

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and
            request.user.role == "PATIENT"
        )


class IsNurse(BasePermission):
    message = "Only nurses can perform this action"

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and
            request.user.role == "NURSE"
        )