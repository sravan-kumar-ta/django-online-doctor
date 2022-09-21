from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from rest_framework_simplejwt.tokens import RefreshToken


AUTH_PROVIDERS = {
    'email': 'email',
    'google': 'google',
}


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
    auth_provider = models.CharField(max_length=100, blank=False, null=False,
                                     default=AUTH_PROVIDERS.get('email'))

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def tokens(self):
        refresh = RefreshToken.for_user(self)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        }
