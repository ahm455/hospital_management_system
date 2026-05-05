from core.models import Appointment
from django.contrib import admin
from .models import *

admin.site.register(User)
admin.site.register(Staff)
admin.site.register(Patient)
admin.site.register(Doctor)
admin.site.register(Nurse)