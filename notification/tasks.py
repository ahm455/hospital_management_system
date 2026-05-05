from celery import shared_task
from django.core.mail import send_mail

@shared_task(bind=True, max_retries=3)
def send_email_task(self, subject, message, recipient_list):
    try:
        send_mail(subject,message,"your_email@gmail.com",recipient_list,fail_silently=False,)
        
    except Exception as e:
        raise self.retry(exc=e, countdown=5)