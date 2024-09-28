from django.shortcuts import render, get_object_or_404
from django.contrib.auth import get_user_model
from rest_framework.views import APIView
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework import authentication
from .serializers import CustomUserSerializer, UserLoginSerializer

User = get_user_model()

# Create your views here.
#UserRegistrtaionView
class RegisterUserView(generics.GenericAPIView):
    serializer_class = CustomUserSerializer
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    #Getting data from user registration request

    def post(self, request, format=None):
        username = request.data.get('username')
        email = request.data.get('email')
        password = request.data.get('password')

        #Data validation
        if username is None or password is None:
            return Response({'error': 'Please provide both username and password'},
                            status=status.HTTP_400_BAD_REQUEST)
        if User.objects.filter(username=username).exists():
            return Response({'error': 'Username has already been taken'},
                            status=status.HTTP_400_BAD_REQUEST)
        if User.objects.filter(email=email).exists():
            return Response({'error': 'Email has already been taken'},
                            status=status.HTTP_400_BAD_REQUEST)
        
        #New user creation/registration
        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()
        return Response({'message': 'User created successfully'}, status=status.HTTP_201_CREATED)
    
#UserLoginView
class LoginUserView(generics.GenericAPIView):
    serializer_class = UserLoginSerializer
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, format=None):
        username = request.data.get('username')
        password = request.data.get('password')

        #User validation
        if username is None or password is None:
            return Response({'error': 'Username and password are required to login.'}, status=status.HTTP_400_BAD_REQUEST)
        
        user = get_object_or_404(User, username=username)
        
        if not user.check_password(password):
            return Response({'error': 'Invalid credentials'},status=status.HTTP_404_NOT_FOUND)
        return Response({'message': 'Login successful'}, status=status.HTTP_200_OK)
    
    #UserLogoutView
    def get(self, request, format=None):
        request.user.auth_token.delete()
        return Response({'message': 'Logout successful'}, status=status.HTTP_200_OK)
    
    #UserProfileView
    class UserProfileView(generics.GenericAPIView):
        authentication_classes = [authentication.TokenAuthentication]
        permission_classes = [permissions.IsAuthenticated]          
        serializer = CustomUserSerializer

        #Get user profile
        def get(self, request):
            user = request.user
            data = {
                'username': user.username,
                'email': user.email,
                'bio': user.bio,
                'profile_pic': user.profile_pic.url if user.profile_pic else None,
                'location': user.location,
                'website': user.website,
                'cover_pic': user.cover_pic.url if user.cover_pic else None,
                'followers': user.followers.count(),
                'following': user.following.count()
            }
            return Response(data)
           
        #Update user profile
        def put(self, request):
            user = request.user
            serializer = CustomUserSerializer(user, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response ('message: Profile updated successfully', status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


       
