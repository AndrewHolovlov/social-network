from django.urls import path

from .views import PostView, PostLikeView


urlpatterns = [
    path('', PostView.as_view()),
    path('<int:post_id>/like/', PostLikeView.as_view()),
]
