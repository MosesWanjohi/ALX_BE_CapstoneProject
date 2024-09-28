from .models import CustomUser
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
        user = get_user_model().objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            bio = validated_data['bio'],
            profile_pic = validated_data['profile_pic'],
            location = validated_data['location'],
            website = validated_data['website'],
            cover_pic = validated_data['cover_pic'],
            )
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