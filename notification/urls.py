from django.urls import path
from .models import Notification
from .views import *

app_name = 'notification'

urlpatterns = [
    path("", NotificationListView.as_view(), name="notification-list"),
    path("<int:pk>/read/",MarkNotificationReadView.as_view(),name="notification-mark-read",),
    path("read-all/",MarkAllNotificationsReadView.as_view(),name="notification-mark-all-read",),
]
