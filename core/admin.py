from django.contrib import admin
from .models import *
from simple_history.admin import SimpleHistoryAdmin

admin.site.register(Appointment, SimpleHistoryAdmin)
admin.site.register(Vitals, SimpleHistoryAdmin)
admin.site.register(Prescription, SimpleHistoryAdmin)
admin.site.register(LabReport, SimpleHistoryAdmin)

# Register your models here.
