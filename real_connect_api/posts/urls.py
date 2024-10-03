
from django.urls import path, include
from .views import PostViewSet, FeedView
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token


#posts/urls.py
#Creating router for registering the PostViewSet

router = DefaultRouter()
router.register(r'posts', PostViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('api-token-auth/', obtain_auth_token),
    path('feed/', FeedView.as_view(), name='feed'),
]
