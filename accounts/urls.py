from django.urls import path
from accounts import views


urlpatterns = [
    path('register/', views.CustomUserCreationView.as_view(), name="register"),
    path('doctor-registration/<int:d_id>/', views.add_doctor_specialisation, name="doctor-register"),
    path('login/', views.LoginView.as_view(), name="login"),
    path('logout/', views.sign_out_view, name="logout"),
]
