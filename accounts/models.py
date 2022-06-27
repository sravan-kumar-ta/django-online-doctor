from django.contrib.auth.models import AbstractUser
from django.db import models


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
    gender = models.CharField(choices=gender_options, max_length=20)
    age = models.PositiveIntegerField(null=True)

    def __str__(self):
        return self.username
