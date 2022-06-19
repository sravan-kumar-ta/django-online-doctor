from django.contrib import admin
from accounts.models import CustomUser, Specialities, Doctors, Patients


# Register your models here.
admin.site.register(CustomUser)
admin.site.register(Specialities)
admin.site.register(Doctors)
admin.site.register(Patients)