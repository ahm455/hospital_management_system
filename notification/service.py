from .models import Notification
from .tasks import send_email_task


def create_notification(user, title, message, type):
    if Notification.objects.filter(user=user,title=title,message=message,type=type).exists():
        return None

    notification = Notification.objects.create(user=user,title=title,message=message,type=type)
    
    send_email_task.delay(subject=title,message=message,recipient_list=[user.email])


    return notification