import datetime

from rest_framework import generics, status, exceptions
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from django.db.models import Count, Exists, OuterRef

from .models import Post, Like
from .serializers import PostSerializer, LikeSerializer


class PostView(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (IsAuthenticated,)

    def list(self, request, *args, **kwargs):
        is_liked = Like.objects.filter(
            post=OuterRef('pk'),
            user=request.user.id)
        queryset = self.queryset.annotate(number_of_likes=Count('likes'), is_liked=Exists(is_liked))
        return Response(self.serializer_class(queryset, many=True).data)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['user'] = self.request.user
        return context


class PostLikeView(APIView):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer
    permission_classes = (IsAuthenticated,)

    @swagger_auto_schema(
        operation_id='Like a post by id',
        responses={
            200: LikeSerializer,
            404: 'Post does not exist',
            400: 'You already liked this post'
        }
    )
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

    @swagger_auto_schema(
        operation_id='Unlike a post by id',
        responses={
            204: "",
            404: 'Post does not exist',
            400: 'You did not like this post'
        }
    )
    def delete(self, request, post_id: int):
        user = request.user
        if not Post.objects.filter(id=post_id).exists():
            raise exceptions.NotFound('Post does not exist')
        if not Like.objects.filter(post_id=post_id, user=user).exists():
            raise exceptions.ValidationError('You did not like this post')
        Like.objects.get(post_id=post_id, user=user).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class AnalyticsLikeView(APIView):

    @swagger_auto_schema(
        operation_id='likes_analytics',
        operation_description='Get likes analytics between given dates in the next format: YYYY-mm-dd',
        manual_parameters=[
            openapi.Parameter(name='date_from', in_=openapi.IN_QUERY, type=openapi.TYPE_STRING, required=True,
                              format='date'),
            openapi.Parameter(name='date_to', in_=openapi.IN_QUERY, type=openapi.TYPE_STRING, format='date'),
        ],
        responses={
            200: openapi.Schema(type=openapi.TYPE_OBJECT,
                                properties={'number_of_likes': openapi.Schema(type=openapi.TYPE_INTEGER)}),
            400: 'Invalid query params, date_to must be greater than date_from'
        }
    )
    def get(self, request):
        date_from = request.query_params.get('date_from', None)
        if not date_from:
            number_of_likes = Like.objects.count()
        else:
            date_to = request.query_params.get('date_to', datetime.datetime.now())
            if date_from > date_to:
                return Response(
                    "Invalid query params, date_to must be greater than date_from",
                    status=status.HTTP_400_BAD_REQUEST)
            number_of_likes = Like.objects.filter(created_at__range=(date_from, date_to)).count()
        return Response({'number_of_likes': number_of_likes}, status=status.HTTP_200_OK)

