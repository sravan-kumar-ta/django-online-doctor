from django.contrib.auth import views as auth_views
from django.urls import path
from accounts import views

urlpatterns = [
    path('register/', views.CustomUserCreationView.as_view(), name="user-registration"),
    path('login/', views.LoginView.as_view(), name="user_login"),
    path('logout/', views.sign_out_view, name="user_logout"),
    path('select_role/', views.user_role_check, name="select-role"),

    path('reset_password/', auth_views.PasswordResetView.as_view(template_name='account/password_reset.html'),
         name='password_reset'),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(
        template_name='account/password_reset_sent.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='account/password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(
        template_name='account/password_reset_done.html'), name='password_reset_complete'),
]
