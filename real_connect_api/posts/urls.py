
from django.urls import path, include
from .views import PostViewSet, FeedView, LikePostView, CommentViewSet
from rest_framework.routers import DefaultRouter


#posts/urls.py
#Creating router for registering the PostViewSet

router = DefaultRouter()
router.register(r'posts', PostViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('feed/', FeedView.as_view(), name='feed'),
    path('posts/<int:pk>/like/', LikePostView.as_view(), name='like-post'),

    path('posts/<int:pk>/comments/', CommentViewSet.as_view({'get': 'list', 'post': 'create'}), name='post-comments'),
    path('posts/<int:pk>/comments/<int:comment_id>/', CommentViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='comment-detail'),
]