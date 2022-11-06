from django.contrib import admin
from patients.models import Appointments


# Register your models here.
class AppointmentsAdmin(admin.ModelAdmin):
    list_display = ['id', 'patient', 'doctor', 'date_time_start']


admin.site.register(Appointments, AppointmentsAdmin)
