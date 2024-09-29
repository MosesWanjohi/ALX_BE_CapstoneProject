from django.urls import path, include
from .views import RegisterUserView, LoginUserView, LogoutUserView, UserProfileView

urlpatterns = [
    path('register/', RegisterUserView.as_view(), name='register'), 
    path('login/', LoginUserView.as_view(), name='login'),
    path('logout/', LogoutUserView.as_view(), name='logout'),
    path('profile/', UserProfileView.as_view(), name='profile'),
]
