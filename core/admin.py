from django.contrib import admin
from .models import *

admin.site.register(Appointment)
admin.site.register(Vitals)
admin.site.register(LabReport)
admin.site.register(Prescription)
# Register your models here.
