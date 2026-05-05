from users.models import *
from services.constants import *
from services.common import *

class Appointment(TimeStamp):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name="appointment")
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name="appointment")
    scheduled_at = models.DateTimeField()
    reason=models.CharField(max_length=100,null=True,blank=True)
    status = models.CharField(choices=AppointmentChoices.choices,max_length=10,default=AppointmentChoices.SCHEDULED)

    def __str__(self):
        return f"{self.doctor} {self.patient}"


class Vitals(TimeStamp):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name="vitals")
    recorded_by = models.ForeignKey(Nurse, on_delete=models.CASCADE, related_name="vitals")
    history = models.CharField(max_length=100,null=True,blank=True)
    pulse = models.IntegerField()
    temperature = models.FloatField()
    weight = models.FloatField()
    blood_pressure = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.patient} {self.recorded_by}"

class Prescription(TimeStamp):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name="prescription")
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name="prescription")
    appointment=models.OneToOneField(Appointment, on_delete=models.CASCADE, related_name="prescription")
    medication = models.CharField(max_length=100)
    notes=models.CharField(max_length=100,null=True,blank=True)

    def __str__(self):
        return f"{self.patient}, Doctor : {self.doctor}, {self.medication} ,{self.notes}"

class LabReport(TimeStamp):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name="lab_report")
    ordered_by=models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name="lab_report")
    test_name=models.CharField(max_length=100,null=True,blank=True)
    result=models.CharField(max_length=100,null=True,blank=True)
    status=models.CharField(max_length=20,choices=LabReportChoices.choices,default=LabReportChoices.PENDING,null=True,blank=True)

    def __str__(self):
        return f"{self.patient} {self.ordered_by}"