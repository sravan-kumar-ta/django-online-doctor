from django.urls import path
from doctors import views

app_name = 'doctor'

urlpatterns = [
    path('profile/', views.profile, name='profile'),
    path('doctor-registration', views.add_doctor_details, name="doctor-register"),
]
