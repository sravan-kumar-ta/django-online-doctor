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
