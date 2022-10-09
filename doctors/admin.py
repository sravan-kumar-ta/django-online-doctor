from django.contrib import admin
from doctors.models import Doctors, Specialities


# Register your models here.
class SpecialitiesAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ["title", ]}


class DoctorsAdmin(admin.ModelAdmin):
    list_display = ('details', 'specialized_in')


admin.site.register(Specialities, SpecialitiesAdmin)
admin.site.register(Doctors, DoctorsAdmin)
