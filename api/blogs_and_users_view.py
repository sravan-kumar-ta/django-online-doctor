from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.generics import CreateAPIView, UpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from api.serializers import PostSerializer, UserSerializer, CustomUserSerializer, ChangePasswordSerializer
from blogs.models import Posts


class PostViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated, ]
    serializer_class = PostSerializer
    queryset = Posts.objects.all()

    def create(self, request, *args, **kwargs):
        if request.user.role == 'doctor':
            serializer = self.serializer_class(data=request.data, context={'user': request.user})
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_406_NOT_ACCEPTABLE)
        else:
            return Response({'message': 'Only doctors can create a blog.'}, status=status.HTTP_406_NOT_ACCEPTABLE)

    def is_author(self):
        instance = self.get_object()
        author = instance.author
        if self.request.user == author:
            return True

    def update(self, request, *args, **kwargs):
        if self.is_author():
            return super().update(request, *args, **kwargs)
        else:
            return Response({'message': 'Only authors can edit post.'}, status=status.HTTP_406_NOT_ACCEPTABLE)

    def destroy(self, request, *args, **kwargs):
        if self.is_author():
            return super().destroy(request, *args, **kwargs)
        else:
            return Response({'message': 'Only authors can delete a post.'}, status=status.HTTP_401_UNAUTHORIZED)

    @action(['GET'], detail=False)
    def get_my_posts(self, request):
        posts = Posts.objects.all()
        my_posts = posts.filter(author=request.user)
        serializer = self.get_serializer(my_posts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(['GET'], detail=True)
    def get_likes(self, request, *args, **kwargs):
        post = self.get_object()
        liked_users = post.likes.all()
        serializer = UserSerializer(liked_users, many=True)
        return Response(serializer.data)

    @action(['POST'], detail=True)
    def like_or_dislike(self, request, *args, **kwargs):
        post = self.get_object()
        user = self.request.user
        liked_users = post.likes.all()
        if user in liked_users:
            post.likes.remove(user)
            post.save()
            return Response({'message': 'Post disliked'}, status=status.HTTP_200_OK)
        else:
            post.likes.add(user)
            post.save()
            return Response({'message': 'Post liked'}, status=status.HTTP_201_CREATED)


class CreateUserView(CreateAPIView):
    model = get_user_model()
    serializer_class = CustomUserSerializer


class UserAPIView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CustomUserSerializer

    def get(self, request, *args, **kwargs):
        user = self.request.user
        serializer = self.serializer_class(user)
        return Response(serializer.data)

    def patch(self, request, *args, **kwargs):
        doctor = request.user
        serializer = self.serializer_class(instance=doctor, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_205_RESET_CONTENT)
        else:
            return Response({'error_message': 'invalid data'}, status=status.HTTP_406_NOT_ACCEPTABLE)


class ChangePasswordView(UpdateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = ChangePasswordSerializer

    def update(self, request, *args, **kwargs):
        user = request.user
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            if not user.check_password(serializer.data.get('old_password')):
                return Response(
                    {'error_message': 'you entered old password is wrong'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            user.set_password(serializer.data.get('new_password'))
            user.save()
            return Response(
                {'success_message': 'password updated successfully'},
                status=status.HTTP_205_RESET_CONTENT
            )
        else:
            return Response({'message': 'invalid data'}, status=status.HTTP_400_BAD_REQUEST)
