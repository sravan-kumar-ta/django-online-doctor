from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.generics import CreateAPIView, UpdateAPIView, GenericAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from accounts.models import CustomUser
from api.serializers import PostSerializer, UserSerializer, CustomUserSerializer, ChangePasswordSerializer, \
    LogoutSerializer, LoginSerializer
from blogs.models import Posts


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 6


class PostViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated, ]
    serializer_class = PostSerializer
    queryset = Posts.objects.all()
    pagination_class = StandardResultsSetPagination

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
        queryset = self.get_queryset().filter(author=request.user)
        page = self.paginate_queryset(queryset)
        serializer = self.get_serializer(page, many=True)
        return self.get_paginated_response(serializer.data)

    @action(['GET'], detail=True)
    def get_likes(self, request, *args, **kwargs):
        post = self.get_object()
        liked_users = post.likes.all()
        serializer = UserSerializer(liked_users, many=True)
        return Response(serializer.data)

    @action(['GET'], detail=True)
    def like_or_dislike(self, request, *args, **kwargs):
        post = self.get_object()
        user = self.request.user
        liked_users = post.likes.all()
        if user in liked_users:
            post.likes.remove(user)
            post.save()
            return Response({'message': 'not liked', 'total_likes': post.total_likes()}, status=status.HTTP_200_OK)
        else:
            post.likes.add(user)
            post.save()
            return Response({'message': 'liked', 'total_likes': post.total_likes()}, status=status.HTTP_201_CREATED)

    @action(['GET'], detail=True)
    def liked_or_not(self, request, *args, **kwargs):
        post = self.get_object()
        liked_users = post.likes.all()
        if request.user in liked_users:
            return Response({'message': 'liked'})
        return Response({'message': 'not liked'})

    # @action(['GET'], detail=True)
    # def is_user(self, request, *args, **kwargs):
    #     post = self.get_object()
    #     if post.author == request.user:
    #         return Response({'is_user': true})
    #     liked_users = post.likes.all()
    #     serializer = UserSerializer(liked_users, many=True)
    #     return Response(serializer.data)


class CreateUserView(CreateAPIView):
    model = get_user_model()
    serializer_class = CustomUserSerializer


class LoginAPIView(GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserAPIView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer

    def get(self, request, *args, **kwargs):
        user = self.request.user
        serializer = self.serializer_class(user)
        return Response(serializer.data)

    def patch(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            instance=request.user,
            data=request.data,
            partial=True,
            context={'user': request.user}
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response({'error_message': serializer.errors}, status=status.HTTP_406_NOT_ACCEPTABLE)


class GetUserAPIView(APIView):
    # permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer

    def get(self, request, *args, **kwargs):
        user = CustomUser.objects.get(id=kwargs['id'])
        serializer = self.serializer_class(user)
        return Response(serializer.data)


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


class LogoutAPIView(GenericAPIView):
    serializer_class = LogoutSerializer
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(status=status.HTTP_204_NO_CONTENT)
