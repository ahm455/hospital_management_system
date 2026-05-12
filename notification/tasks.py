from celery import shared_task
from django.core.mail import send_mail
from hospital_management_system import settings


@shared_task(bind=True, max_retries=3)
def send_email_task(self, subject, message, recipient_list):
    try:
        send_mail(subject,message,settings.DEFAULT_FROM_EMAIL,recipient_list,fail_silently=False,)
        
    except Exception as e:
        countdown=5 * (2 ** self.request.retries)
        raise self.retry(exc=e, countdown=countdown)