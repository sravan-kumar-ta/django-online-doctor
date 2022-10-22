from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView

from api.blogs_and_users_view import (
    PostViewSet,
    CreateUserView,
    UserAPIView,
    ChangePasswordView,
    LoginAPIView,
    LogoutAPIView,
    GetUserAPIView,
)
from api.patient_view import (
    FamilyMemberViewSet,
    AvailableDateView,
    AvailableTimeView,
    AppointmentViewSet,
    DoctorsListView,
    DoctorView
)
from api import doctor_view as dr_view
from api.doctor_view import DoctorDetailsView, SpecialitiesView
from api.social_auth_view import GoogleSocialAuthView

router = DefaultRouter()
router.register('posts', PostViewSet, basename='posts')
router.register('family_members', FamilyMemberViewSet, basename='family-members')
router.register('appointment', AppointmentViewSet, basename='appointment')

urlpatterns = [
    path('user/register/', CreateUserView.as_view()),
    path('login/', LoginAPIView.as_view()),
    path('user/', UserAPIView.as_view()),
    path('user_by_id/<int:id>/', GetUserAPIView.as_view()),
    path('change_password/', ChangePasswordView.as_view()),
    path('password_reset/', include('django_rest_passwordreset.urls', namespace='password_reset')),
    path('google/', GoogleSocialAuthView.as_view()),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('logout/', LogoutAPIView.as_view()),

    path('specialities/', SpecialitiesView.as_view()),
    path('doctors/<int:sp_id>/', DoctorsListView.as_view()),
    path('doctor/<int:doc_id>/', DoctorView.as_view()),
    path('dates/<int:doc_id>/', AvailableDateView.as_view()),
    path('times/<int:doc_id>/<str:a_date>/', AvailableTimeView.as_view()),
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
# (PUT) api/change_password/ => change password
# (POST) api/password_reset/ => reset password
# (POST) api/password_reset/confirm/ => reset password confirm
# (POST) api/google/ => google authentication
# (POST) api/token/refresh/ => refresh token
# (POST) api/logout/ => logout
#  -----Blog-----
# (GET) api/posts/ => get all post
# (POST) api/posts/ => create new post
# (GET) api/posts/11/ => get single post
# (DELETE) api/posts/11/ => delete a post
# (PUT) api/posts/11/ => update a post
# (PATCH) api/posts/11/ => update a specific field post
# (GET) api/posts/get_my_posts/ => get request user's post
# (GET) api/posts/25/get_likes/ => get likes of a post
# (POST) api/posts/25/like_or_dislike/ => like or dislike post
#  -----Family member-----
# (POST) api/family_members/ => add a family member
# (GET) api/family_members/ => get family members
# (GET) api/family_members/6/ => get family member
# (PUT) api/family_members/6/ => update a family member
# (DELETE) api/family_members/6/ => delete a family member
#  -----Patient-----
# (GET) api/specialities/ => get all specialities
# (GET) api/doctors/7/ => get doctors by specialities
# (GET) api/doctor/7/ => get doctor
# (GET) api/dates/7/ => get available all date time
# (GET) api/times/7/2022-08-11/ => get available date time
# (POST) api/appointment => create an appointment
# (GET) api/appointment => get my all appointment
# (GET) api/appointment/44/ => get my single appointment
# (PATCH) api/appointment/44/ => update status of an appointment
#  -----Doctor-----
# (GET) api/doctor/ => get doctors details
# (POST) api/doctor/ => create doctors details
# (PUT) api/doctor/ => update doctors details
# (GET) api/appointments/upcoming/ => get upcoming appointments
# (GET) api/appointments/active/ => get active appointments
# (GET) api/appointments/completed/ => get completed appointments
# (GET) api/myblogs/ => get blogs created by requested doctor
