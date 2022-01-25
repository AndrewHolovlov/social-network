from django.urls import path

from .views import PostView, PostLikeView, AnalyticsLikeView


urlpatterns = [
    path('', PostView.as_view()),
    path('<int:post_id>/', PostView.as_view()),
    path('<int:post_id>/like/', PostLikeView.as_view()),
    path('analytics/', AnalyticsLikeView.as_view())
]
