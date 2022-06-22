from django.contrib import admin
from accounts.models import CustomUser, Specialities


# Register your models here.
admin.site.register(CustomUser)
admin.site.register(Specialities)
