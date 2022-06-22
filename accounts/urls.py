from django.urls import path
from accounts import views


urlpatterns = [
    path('', views.HomeView.as_view(), name="home"),
    path('register/', views.DoctorRegistrationView.as_view(), name="register"),
    path('login/', views.LoginView.as_view(), name="login"),
    path('logout/', views.sign_out_view, name="logout"),


    path('doctors/', views.doctors, name="doctors"),
    path('profile/', views.profile, name="profile"),
]
