from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView

from api.blogs_and_users_view import PostViewSet, CreateUserView, UserAPIView, ChangePasswordView

router = DefaultRouter()
router.register('posts', PostViewSet, basename='posts')

urlpatterns = [
    path('get_token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('user/register/', CreateUserView.as_view()),
    path('user/', UserAPIView.as_view()),
    path('change_password/', ChangePasswordView.as_view()),
    path('password_reset/', include('django_rest_passwordreset.urls', namespace='password_reset')),
] + router.urls

# http://localhost:8000/...
# (POST) api/get_token/ => get token

# (POST) api/user/register/ => create user
# (GET) api/user/ => get user
# (PATCH) api/user/ => update user
# (PUT) api/change_password/ => change password
# (POST) api/password_reset/ => reset password
# (POST) api/password_reset/confirm/ => reset password confirm

# (GET) api/posts/ => get all post
# (POST) api/posts/ => create new post
# (GET) api/posts/11/ => get single post
# (DELETE) api/posts/11/ => delete a post
# (PUT) api/posts/11/ => update a post
# (PATCH) api/posts/11/ => update a specific field post
# (GET) api/posts/get_my_posts/ => get request user's post
# (GET) api/posts/25/get_likes/ => get likes of a post
# (POST) api/posts/25/like_or_dislike/ => like or dislike post
