from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.
class CustomUser(AbstractUser):
    role_options = (
        ('admin', "Admin"),
        ('doctor', "Doctor"),
        ('patient', "Patient"),
    )
    role = models.CharField(choices=role_options, default="admin", max_length=30)

    def __str__(self):
        return self.username


class Specialities(models.Model):
    special = models.CharField(max_length=50)

    def __str__(self):
        return self.special

    class Meta:
        verbose_name_plural = "Specialities"


class Doctors(models.Model):
    gender_options = (
        ("male", "Male"),
        ("female", "Female"),
    )
    role = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    profile_image = models.ImageField(upload_to='files/doctors')
    gender = models.CharField(choices=gender_options, max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    specialized_in = models.ForeignKey(Specialities, on_delete=models.CASCADE)

    def __str__(self):
        return self.role.username


class Patients(models.Model):
    gender_options = (
        ("male", "Male"),
        ("female", "Female"),
    )
    role = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    profile_image = models.ImageField(upload_to='files/patients')
    gender = models.CharField(choices=gender_options, max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.role.username
