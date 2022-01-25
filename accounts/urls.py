from rest_framework_simplejwt.views import TokenRefreshView

from django.urls import path

from accounts.views import SignUpView, LoginView, AllUsersActivityView, UserActivityView

urlpatterns = [
    path('signup/', SignUpView.as_view()),
    path('login/', LoginView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('users_activity/', AllUsersActivityView.as_view(), name='users activity'),
    path('<int:user_id>/users_activity/', AllUsersActivityView.as_view(), name='users activity'),
    path('activity/', UserActivityView.as_view(), name='users activity'),
]
