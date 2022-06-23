from django.urls import path
from patients import views

app_name = 'patient'

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('<str:s_slug>/doctors/', views.DoctorsListView.as_view(), name='doctors'),


    # path('doctors/', views.doctors, name="doctors"),
    path('profile/', views.profile, name="profile"),
]
