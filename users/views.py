from typing import cast
from rest_framework import generics
from rest_framework.exceptions import PermissionDenied
from services.common import is_staff
from .models import *
from .serializers import UserSerializer


class UserCreateList(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_queryset(self):
        user = cast(User, self.request.user)

        if is_staff(user):
            return User.objects.all()

        return User.objects.filter(id=user.id)

    def perform_create(self, serializer):
        user = cast(User, self.request.user)

        if not is_staff(user):
            raise PermissionDenied("Only staff can create")

        serializer.save()


class UserUpdateDelete(generics.RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_queryset(self):
        user = cast(User, self.request.user)

        if is_staff(user):
            return User.objects.all()

        return User.objects.filter(id=user.id)

    def perform_update(self, serializer):
        user = cast(User, self.request.user)

        if not is_staff(user):
            raise PermissionDenied("Only staff can update")

        serializer.save()

