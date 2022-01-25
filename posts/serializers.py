from rest_framework import serializers

from .models import Post, Like


class PostSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    number_of_likes = serializers.IntegerField(read_only=True, default=0)
    is_liked = serializers.BooleanField(read_only=True, default=False)

    class Meta:
        model = Post
        fields = ['id', 'title', 'content', 'created_at', 'user', 'number_of_likes', 'is_liked']

    def validate(self, attrs):
        user = self.context.get('user')
        attrs['user'] = user
        return attrs


class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ['post', 'user', 'created_at']
