from django.contrib import admin
from patients.models import FamilyMembers, Appointments


# Register your models here.
admin.site.register(FamilyMembers)
admin.site.register(Appointments)
