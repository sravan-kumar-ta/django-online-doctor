from django.contrib import admin
from accounts.models import CustomUser, Specialities


# Register your models here.
class SpecialitiesAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ["special", ]}


admin.site.register(Specialities, SpecialitiesAdmin)
admin.site.register(CustomUser)
