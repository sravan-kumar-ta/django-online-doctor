from django.urls import path
from django.views.generic import TemplateView

from patients import views

app_name = 'patient'

urlpatterns = [
    path('', TemplateView.as_view(template_name='starter.html')),
    path('home/', views.HomeView.as_view(), name='home'),
    path('<str:s_slug>/doctors/', views.DoctorsListView.as_view(), name='doctors'),
    path('profile/', views.UserProfileView.as_view(), name='profile'),
    path('profile/patient/<int:p_id>/update/', views.UpdatePatientView.as_view(), name='patient-update'),
    path('appointments/', views.AppointmentsListView.as_view(), name='appointments'),
    path('find-available-slot/doctor/ajax/', views.available_slot, name='available-slot'),
    path('create_appointment/ajax/<int:d_id>/<str:app_date>/<str:start_time>/', views.create_appointment,
         name='create-appointment'),

    path('demo_appointment/', views.demo_appointment, name='demo-appointment')
]
