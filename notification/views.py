from django.shortcuts import render
from rest_framework import generics
from rest_framework.response import Response
from .models import Notification
from .serializers import NotificationSerializer

class NotificationListView(generics.ListAPIView):
    serializer_class = NotificationSerializer

    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user)

class MarkNotificationReadView(generics.UpdateAPIView):
    serializer_class = NotificationSerializer

    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user)

    def update(self, request, *args, **kwargs):
        notification = self.get_object()
        notification.is_read = True
        notification.save()
        return Response({"message": "Notification marked as read"})


class MarkAllNotificationsReadView(generics.GenericAPIView):

    def patch(self, request, *args, **kwargs):
        Notification.objects.filter(user=request.user,is_read=False).update(is_read=True)

        return Response({"message": "All notifications marked as read"})