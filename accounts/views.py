from rest_framework import generics, status
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.serializers import TokenRefreshSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from .serializers import LoginSerializer, SignUpSerializer, UserActivitySerializer
from .models import User


class LoginView(TokenObtainPairView):
    permission_classes = (AllowAny,)
    serializer_class = LoginSerializer

    @swagger_auto_schema(
        operation_id="login",
        request_body=LoginSerializer,
        responses={201: TokenRefreshSerializer, 400: "Bad request"},
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class SignUpView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = SignUpSerializer

    @swagger_auto_schema(
        operation_id="sign_up",
        request_body=SignUpSerializer,
        responses={201: TokenRefreshSerializer, 400: "Bad request"},
    )
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token = User.get_tokens_for_user(user)
            return Response(token, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AllUsersActivityView(generics.ListAPIView):
    queryset = User.objects.all()
    permission_classes = (IsAdminUser,)
    serializer_class = UserActivitySerializer

    @swagger_auto_schema(
        operation_id="user_activity",
        operation_description="Get last login and last activity dates for each user or one user",
        manual_parameters=[
            openapi.Parameter(name='user_id', in_=openapi.IN_QUERY, type=openapi.TYPE_INTEGER, required=False),
        ],
    )
    def list(self, request, user_id=None, *args, **kwargs):
        if user_id:
            try:
                user = User.objects.get(id=user_id)
            except User.DoesNotExist:
                return Response('User not found', status=status.HTTP_404_NOT_FOUND)
            return Response(self.serializer_class(user).data, status=status.HTTP_200_OK)
        else:
            return Response(self.serializer_class(self.get_queryset(), many=True).data, status=status.HTTP_200_OK)


class UserActivityView(generics.RetrieveAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = UserActivitySerializer

    @swagger_auto_schema(
        operation_id="activity_for_user",
        operation_description="Get last login and last activity dates for the given user",
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def get_object(self):
        return self.request.user
