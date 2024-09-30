from .models import CustomUser, UserProfile, Role, UserRole
from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token

#Creating CustomUserSerializer
class CustomUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password']
    
    #User Creation 
    def create(self, validated_data):
        #Creating User
        user = get_user_model().objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],      

        )
        user.save()


        #Creating an empty User Profile as soon as user is created
        UserProfile.objects.create(user=user)
        #Creating Token for the new user
        Token.objects.create(user=user)
        
    #Assigning default role to the user upon registration
        try:
            regular_role = Role.objects.get(name="regular")
            UserRole.objects.create(user=user, role=regular_role)
        except Role.DoesNotExist:
            raise serializers.ValidationError("Default role 'regular'does not exist. Please create it.")
        
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


#Role Serializer
class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = ['name']

    #Validation to prevent duplicating roles
    def validate(self, data):
        if Role.objects.filter(name=data['name']).exists():
            raise serializers.ValidationError("Role already exists")
        return data

#UserRole Serializer for displaying roles for a user
class UserRoleSerializer(serializers.ModelSerializer):
    role = RoleSerializer(read_only=True)
    
    class Meta:
        model = UserRole
        fields = [ 'role', 'assigned_at']


#User Profile Serializer
class UserProfileSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer(read_only=True)
    roles = serializers.SerializerMethodField() #Fetch roles dynamically
    
    class Meta:
        model = UserProfile
        fields = ['user', 'bio', 'profile_pic', 'cover_pic', 'company_name', 'location', 'website',  'specialization', 'roles']

    #Getting all roles assigned to a user (A user can have multiple roles)
    def get_roles(self, obj):
        user_roles = UserRole.objects.filter(user=obj.user)
        return UserRoleSerializer(user_roles, many=True).data
    
    #Updating User Profile
    def update(self, instance, validated_data):
        instance.bio = validated_data.get('bio', instance.bio)
        instance.profile_pic = validated_data.get('profile_pic', instance.profile_pic)
        instance.cover_pic = validated_data.get('cover_pic', instance.cover_pic)
        instance.company_name = validated_data.get('company_name', instance.company_name)
        instance.location = validated_data.get('location', instance.location)
        instance.website = validated_data.get('website', instance.website)
        instance.specialization = validated_data.get('specialization', instance.specialization)
        instance.save()

        #fetching user and updating user fields if user data is provided in the request context
        user_data = self.context['request'].data.get('user', None)

        if user_data:
            user = instance.user
            #Update of the related CustomUser fields
            user.username = user_data.get('username', user.username)
            user.email = user_data.get('email', user.email)
            user.save()
        return instance
        
        
        
        
        
        
        
        
        
        
        
        
        
       