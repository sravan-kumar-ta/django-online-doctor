from django.urls import path
from accounts import views


urlpatterns = [
    path('register/', views.CustomUserCreationView.as_view(), name="user-registration"),
    path('login/', views.LoginView.as_view(), name="login"),
    path('logout/', views.sign_out_view, name="logout"),
    path('select_role/', views.user_role_check, name="select-role"),
]
