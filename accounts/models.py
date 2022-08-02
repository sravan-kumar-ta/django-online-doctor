from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


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
    email = models.EmailField(_("email address"), unique=True)
    role = models.CharField(choices=role_options, default="admin", max_length=30)
    gender = models.CharField(choices=gender_options, max_length=20)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
