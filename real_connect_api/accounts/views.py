from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework import authentication
from .serializers import (
    CustomUserSerializer,
    UserLoginSerializer,
    RoleSerializer,
    UserRoleSerializer,
    UserProfileSerializer
)
from rest_framework.authtoken.models import Token
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
        print("Request data: ", request.data) #To help debug incoming data
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'User registered successfully'}, status=status.HTTP_201_CREATED)
        
        #print errors if invalid
        print("Serializer errors: ", serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#UserLoginView
class LoginUserView(generics.GenericAPIView):
    serializer_class = UserLoginSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request, format=None):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data

        #Get or create token for the authenticated user
        token, created = Token.objects.get_or_create(user=user)

        #Returning the token in the response
        return Response({
            'message': 'Logged in successfully',
            'token': token.key
        }, status=status.HTTP_200_OK)

#UserLogoutView
class LogoutUserView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [authentication.TokenAuthentication]
    
    def get_serializer_class(self):
        #Return None to indicate no serializer is needed
        return None
    
    
    @swagger_auto_schema(
        operation_description="Logout user",
    )

    def post(self, request, *args, **kwargs):
        #Delete the token
        try:
            token = Token.objects.get(user=request.user)
            token.delete()
            return Response({'message': 'Logged out successfully'}, status=status.HTTP_200_OK)

        except Token.DoesNotExist:
            return Response({'message': 'Token not found'}, status=status.HTTP_404_BAD_REQUEST)
    
#UserProfileView
class UserProfileView(generics.GenericAPIView):
    authentication_classes = [authentication.TokenAuthentication]
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


       
