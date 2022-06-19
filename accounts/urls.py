from django.urls import path
from accounts import views


urlpatterns = [
    path('', views.home, name="home"),
    path('doctors/', views.doctors, name="doctors"),
    path('profile/', views.profile, name="profile"),
]
