from .models import CustomUser, UserProfile
from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token

#Creating CustomUserSerializer
class CustomUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password', 'bio', 'profile_pic', 'location', 'website', 'cover_pic']
        
    #User Creation 
    def create(self, validated_data):
        #Creating User without profile first
        user = get_user_model().objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],      

        ) 
        #Additonal fields to the User
        user.bio = validated_data.get('bio', "")
        user.profile_pic = validated_data.get('profile_pic', None)
        user.location = validated_data.get('location', "")
        user.website = validated_data.get('website', "")
        user.cover_pic = validated_data.get('cover_pic', None)
        user.additional_info = validated_data.get('additional_info', "") #Provides room for additional info in future
        user.save()

        #Creating User Profile
        UserProfile.objects.create(user=user, role="regular")
        
        #Creating Token for the new user
        Token.objects.create(user=user)
        return user
    
#User Login Serializer
class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        user = get_user_model().objects.filter(username=data['username']).first()
        if user is None:
            raise serializers.ValidationError("User does not exist")
        if not user.check_password(data['password']):
            raise serializers.ValidationError("Incorrect Password or Credentials")
        return user
    
#User Profile Serializer
class UserProfileSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer(read_only=True)
    class Meta:
        model = UserProfile
        fields = ['user', 'role']
    
    