from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import status, exceptions
from rest_framework.response import Response

from django.http import Http404

from .models import Post, Like
from .serializers import PostSerializer, LikeSerializers


class PostView(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (IsAuthenticated,)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['user'] = self.request.user
        return context


class PostLikeView(APIView):
    queryset = Like.objects.all()
    serializer_class = LikeSerializers
    permission_classes = (IsAuthenticated,)

    def post(self, request, post_id: int):
        user = request.user
        if not Post.objects.filter(id=post_id).exists():
            raise exceptions.NotFound('Post does not exist')
        if Like.objects.filter(post_id=post_id, user=user).exists():
            raise exceptions.ValidationError('You already liked this post')
        serializer = self.serializer_class(data={'user': user.id, 'post': post_id})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, post_id: int):
        user = request.user
        if not Post.objects.filter(id=post_id).exists():
            raise exceptions.NotFound('Post does not exist')
        if not Like.objects.filter(post_id=post_id, user=user).exists():
            raise exceptions.ValidationError('You did not like this post')
        Like.objects.get(post_id=post_id, user=user).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
