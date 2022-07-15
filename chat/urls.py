from django.urls import path
from chat import views

urlpatterns = [
    path('chat_room/<int:app_id>/', views.enter_room, name='chat'),
]

