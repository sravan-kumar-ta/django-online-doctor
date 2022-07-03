from django.urls import path
from doctors import views

app_name = 'doctor'

urlpatterns = [
    path('profile/', views.profile, name='profile'),
    path('profile/patient/<int:dtr_id>/update/', views.UpdatePatientView.as_view(), name='doctor-update'),
    path('doctor-registration', views.add_doctor_details, name="doctor-register"),
    path('details/update/', views.update_details, name="update-details"),
    path('available-time/update/<int:dtr_id>/', views.update_available_time, name="update-times"),
    path('appointments/', views.AppointmentsView.as_view(), name="appointments"),
]
