from os import environ
from celery import Celery

environ.setdefault('DJANGO_SETTINGS_MODULE', 'hospital_management_system.settings')

app = Celery('hospital_management_system')

app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()