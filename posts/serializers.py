from rest_framework import serializers

from .models import Post, Like


class PostSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    # like = serializers.BooleanField(read_only=True)

    class Meta:
        model = Post
        fields = ['id', 'title', 'content', 'created_at', 'user']

    def validate(self, attrs):
        user = self.context.get('user')
        attrs['user'] = user
        return attrs


class LikeSerializers(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ['post', 'user', 'created_at']
