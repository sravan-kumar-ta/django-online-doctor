from django.urls import path
from doctors import views

app_name = 'doctor'

urlpatterns = [
    path('profile/', views.profile, name='profile'),
    path('profile/patient/<int:p_id>/update/', views.UpdatePatientView.as_view(), name='doctor-update'),
    path('doctor-registration', views.add_doctor_details, name="doctor-register"),
    path('details/update/', views.update_details, name="update-details"),
    path('appointments/', views.AppointmentsView.as_view(), name="appointments"),
]
