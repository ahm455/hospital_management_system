from django.db import models
from services.constants import NotificationType
from users.models import User
from users.models import TimeStamp


class Notification(TimeStamp):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    title=models.CharField(max_length=100)
    message=models.TextField()
    type = models.CharField(max_length=20,choices=NotificationType.choices)
    is_read=models.BooleanField(default=False)

    def __str__(self):
        return self.title