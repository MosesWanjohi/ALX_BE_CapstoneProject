from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from .serializers import (
    CustomUserSerializer,
    UserLoginSerializer,
    UserProfileSerializer
)
from .models import UserProfile
from drf_yasg.utils import swagger_auto_schema

User = get_user_model()

#Create your views here.

#UserRegistrationView
class RegisterUserView(generics.GenericAPIView):
    serializer_class = CustomUserSerializer
    permission_classes = [permissions.AllowAny]

    #Registering User
    def post(self, request, format=None):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'User registered successfully'}, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


#UserLoginView
class LoginUserView(generics.GenericAPIView):
    serializer_class = UserLoginSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        if serializer.is_valid():
            user = serializer.validated_data['user']  # Returning the user object
            refresh = RefreshToken.for_user(user)  # Generating the tokens
        
        #Returning the token in the response
            return Response({
                'message': 'Logged in successfully',
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#UserLogoutView
class LogoutUserView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Logout user",
    )

    def post(self, request, *args, **kwargs):
        
        #Blacklisting the refresh token as added layer of security
        if hasattr(request.user, 'refresh_token'):
            request.user.refresh_token.delete()
        return Response({'message': 'Logged out successfully'}, status=status.HTTP_200_OK)


#UserProfileView
class UserProfileView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]          
    serializer_class = UserProfileSerializer

    #Get user profile
    def get(self, request):
        user_profile = get_object_or_404(UserProfile, user=request.user) #Gets the profile of the logged in user
       #If user has no profile the response will be 404
        serializer = self.get_serializer(user_profile)
        return Response(serializer.data, status=status.HTTP_200_OK)

    #Update user profile
    def put(self, request):
        user_profile = get_object_or_404(UserProfile, user=request.user) #Gets the profile of the logged in user
        serializer = self.get_serializer(user_profile, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response ({'message': 'Profile updated successfully'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
    #Delete user profile
    def delete(self, request):
        user_profile = get_object_or_404(UserProfile, user=request.user) #Gets the profile of the logged in user
        user_profile.delete()
        return Response ({'message': 'Profile deleted successfully'}, status=status.HTTP_204_NO_CONTENT)


       
