from django.db import models

from accounts.models import CustomUser
from doctors.models import Doctors


class Appointments(models.Model):
    patient = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="app_patient")
    doctor = models.ForeignKey(Doctors, on_delete=models.CASCADE, related_name="app_doctor")
    date = models.DateField(null=True, blank=True)
    time = models.TimeField(null=True, blank=True)
    date_time_start = models.DateTimeField(null=True, blank=True)
    date_time_end = models.DateTimeField(null=True, blank=True)
