from django.db import models
from django.urls import reverse

from accounts.models import CustomUser


class Specialities(models.Model):
    title = models.CharField(max_length=50, unique=True)
    slug = models.CharField(max_length=50, unique=True)

    def get_url(self):
        return reverse('patient:doctors', args=[self.slug])

    def __str__(self):
        return self.title


class Doctors(models.Model):
    # specialized_choices = (
    #     ('Cardiology', 'Cardiology'),
    #     ('Neurology', 'Neurology'),
    #     ('Ortho / Bone', 'Ortho / Bone'),
    #     ('Oncology', 'Oncology'),
    #     ('pediatrics', 'pediatrics'),
    #     ('ENT', 'ENT'),
    #     ('Eye Specialist', 'Eye Specialist'),
    #     ('Physician', 'Physician'),
    #     ('Dermatology', 'Dermatology'),
    #     ('Psychiatry', 'Psychiatry'),
    #     ('Pulmonology', 'Pulmonology'),
    # )
    details = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='doctor')
    profile_image = models.ImageField(upload_to='images/doctors', null=True)
    specialized_in = models.ForeignKey(Specialities, on_delete=models.CASCADE)
    charge = models.PositiveIntegerField()

    sun_start = models.TimeField(null=True, blank=True)
    sun_end = models.TimeField(null=True, blank=True)

    mon_start = models.TimeField(null=True, blank=True)
    mon_end = models.TimeField(null=True, blank=True)

    tue_start = models.TimeField(null=True, blank=True)
    tue_end = models.TimeField(null=True, blank=True)

    wed_start = models.TimeField(null=True, blank=True)
    wed_end = models.TimeField(null=True, blank=True)

    thu_start = models.TimeField(null=True, blank=True)
    thu_end = models.TimeField(null=True, blank=True)

    fri_start = models.TimeField(null=True, blank=True)
    fri_end = models.TimeField(null=True, blank=True)

    sat_start = models.TimeField(null=True, blank=True)
    sat_end = models.TimeField(null=True, blank=True)

    def get_url(self):
        return reverse('patient:doctors', args=[self.slug])

    def __str__(self):
        return self.details.username
