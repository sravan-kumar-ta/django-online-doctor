from django.contrib.auth.models import AbstractUser
from django.db import models


class Specialities(models.Model):
    special = models.CharField(max_length=50)

    def __str__(self):
        return self.special

    class Meta:
        verbose_name_plural = "Specialities"


class CustomUser(AbstractUser):
    role_options = (
        ('admin', "Admin"),
        ('doctor', "Doctor"),
        ('patient', "Patient"),
    )
    gender_options = (
        ("male", "Male"),
        ("female", "Female"),
    )
    role = models.CharField(choices=role_options, default="admin", max_length=30)
    profile_image = models.ImageField(upload_to='files/doctors', null=True)
    gender = models.CharField(choices=gender_options, max_length=20)
    specialized_in = models.ForeignKey(Specialities, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.username
