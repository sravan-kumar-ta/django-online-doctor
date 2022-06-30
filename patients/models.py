from django.db import models

from accounts.models import CustomUser


class FamilyMembers(models.Model):
    relation_with = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    relation = models.CharField(max_length=50)
    name = models.CharField(max_length=100)
    age = models.PositiveIntegerField()


class Appointments(models.Model):
    status_choices = [
        ("finished", "finished"),
        ("upcoming", "upcoming"),
        ("ongoing", "ongoing"),
    ]
    patient = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="app_patient")
    doctor = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="app_doctor")
    date = models.DateField(null=True, blank=True)
    time = models.TimeField(null=True, blank=True)
    date_time_start = models.DateTimeField(null=True, blank=True)
    date_time_end = models.DateTimeField(null=True, blank=True)
    status = models.CharField(null=True, blank=True, max_length=20, choices=status_choices)
