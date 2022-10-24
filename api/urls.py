from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView

from api import blogs_and_users_view as views
from api import patient_view as pt_view
from api import doctor_view as dr_view
from api.doctor_view import DoctorDetailsView, SpecialitiesView
from api.social_auth_view import GoogleSocialAuthView

router = DefaultRouter()
router.register('posts', views.PostViewSet, basename='posts')
router.register('appointment', pt_view.AppointmentViewSet, basename='appointment')

urlpatterns = [
    path('user/register/', views.CreateUserView.as_view()),
    path('login/', views.LoginAPIView.as_view()),
    path('user/', views.UserAPIView.as_view()),
    path('user_by_id/<int:id>/', views.GetUserAPIView.as_view()),
    path('change_password/', views.ChangePasswordView.as_view()),
    path('password_reset/', include('django_rest_passwordreset.urls', namespace='password_reset')),
    path('google/', GoogleSocialAuthView.as_view()),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('logout/', views.LogoutAPIView.as_view()),

    path('specialities/', SpecialitiesView.as_view()),
    path('doctors/<int:sp_id>/', pt_view.DoctorsListView.as_view()),
    path('doctor/<int:doc_id>/', pt_view.DoctorView.as_view()),
    path('dates/<int:doc_id>/', pt_view.AvailableDateView.as_view()),
    path('times/<int:doc_id>/<str:a_date>/', pt_view.AvailableTimeView.as_view()),
    path('doctor/', DoctorDetailsView.as_view()),
    path('appointments/upcoming/', dr_view.UpcomingAppointmentView.as_view()),
    path('appointments/active/', dr_view.ActiveAppointmentView.as_view()),
    path('appointments/completed/', dr_view.CompletedAppointmentView.as_view()),
] + router.urls

# http://localhost:8000/...
#  -----Account-----
# (POST) api/login/ => login with email and password to get token
# (POST) api/user/register/ => create user
# (GET) api/user/ => get user
# (PATCH) api/user/ => update user
# (PUT) api/change_password/ => change password--------------
# (POST) api/password_reset/ => reset password
# (POST) api/password_reset/confirm/ => reset password confirm
# (POST) api/google/ => google authentication
# (POST) api/token/refresh/ => refresh token
# (POST) api/logout/ => logout--------------
#  -----Blog-----
# (GET) api/posts/?page=<page-number> => get all post
# (POST) api/posts/ => create new post
# (GET) api/posts/11/ => get single post
# (DELETE) api/posts/11/ => delete a post
# (PUT) api/posts/11/ => update a post
# (PATCH) api/posts/11/ => update a specific field post1
# (GET) api/posts/get_my_posts/ => get request user's post1
# (POST) api/posts/25/like_or_dislike/ => like or dislike post
#  -----Patient-----
# (GET) api/specialities/ => get all specialities1
# (GET) api/doctors/7/ => get doctors by specialities
# (GET) api/doctor/7/ => get doctor1
# (GET) api/dates/7/ => get available all date time
# (GET) api/times/7/2022-08-11/ => get available date time1
# (POST) api/appointment => create an appointment1
# (GET) api/appointment => get my all appointment
# (GET) api/appointment/44/ => get my single appointment
# (PATCH) api/appointment/44/ => update status of an appointment
#  -----Doctor-----
# (GET) api/doctor/ => get doctors details1
# (POST) api/doctor/ => create doctors details1
# (PUT) api/doctor/ => update doctors details1
# (GET) api/appointments/upcoming/ => get upcoming appointments1
# (GET) api/appointments/active/ => get active appointments1
# (GET) api/appointments/completed/ => get completed appointments1
# (GET) api/myblogs/ => get blogs created by requested doctor
