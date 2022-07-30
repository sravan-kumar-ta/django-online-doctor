from rest_framework import serializers

from accounts.models import CustomUser
from blogs.models import Posts


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'first_name', 'last_name']
        read_only_fields = fields


class PostSerializer(serializers.ModelSerializer):
    author = UserSerializer(required=False)
    likes = UserSerializer(many=True, required=False)

    class Meta:
        model = Posts
        fields = ('id', 'is_public', 'title', 'content', 'image', 'date', 'author', 'total_likes', 'likes')
        depth = 1

    def create(self, validated_data):
        user = self.context.get('user')
        validated_data['is_public'] = True
        return Posts.objects.create(**validated_data, author=user)


class CustomUserSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = CustomUser
        fields = ['username', 'first_name', 'last_name', 'email', 'gender', 'role', 'password', 'password2']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        password = self.validated_data['password']
        password2 = self.validated_data['password2']
        del validated_data['password2']
        if password != password2:
            raise serializers.ValidationError({'password': 'Passwords must match.'})
        return CustomUser.objects.create_user(**validated_data)
