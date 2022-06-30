from django.urls import path
from patients import views

app_name = 'patient'

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('<str:s_slug>/doctors/', views.DoctorsListView.as_view(), name='doctors'),
    path('add_member/', views.add_family_member_view, name='add_member'),
    path('profile/', views.UserProfileView.as_view(), name='profile'),
    path('profile/member/<int:m_id>/update/', views.UpdateMemberView.as_view(), name='member-update'),
    path('profile/patient/<int:p_id>/update/', views.UpdatePatientView.as_view(), name='patient-update'),
    path('profile/member/<int:m_id>/delete/', views.delete_member, name='member-delete'),


    path('find-available-slot/doctor/ajax/', views.available_slot, name='available-slot'),

    path('create_appointment/ajax/<int:d_id>/<str:app_date>/<str:start_time>/', views.create_appointment,
         name='create-appointment'),




    # path('doctors/', views.doctors, name="doctors"),
    # path('profile/', views.profile, name="profile"),
]
