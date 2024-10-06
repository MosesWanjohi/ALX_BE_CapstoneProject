from .models import CustomUser, UserProfile, Role, UserRole
from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken

# Creating CustomUserSerializer
class CustomUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password']
    
    # User Creation 
    def create(self, validated_data):
        # Creating User
        user = get_user_model().objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
        )
        user.save()

        # Creating an empty User Profile as soon as user is created
        UserProfile.objects.create(user=user)
        self.assign_default_role(user)

        return user

    def assign_default_role(self, user):
        """
        Assigns default role to the user upon registration.
        
        Args:
            user (CustomUser): The user to assign the default role to.
        
        Raises:
            serializers.ValidationError: If the default role 'regular' does not exist.
        """
        try:
            regular_role = Role.objects.get(name="regular")
            UserRole.objects.create(user=user, role=regular_role)
        except Role.DoesNotExist:
            raise serializers.ValidationError("Default role 'regular' does not exist. Please create it.")

# User Login Serializer
class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        user = get_user_model().objects.filter(username=data['username']).first()
        if user is None:
            raise serializers.ValidationError("User does not exist")
        if not user.check_password(data['password']):
            raise serializers.ValidationError("Invalid Credentials")
        
        # Generating JWT tokens
        refresh = RefreshToken.for_user(user)
        access = AccessToken.for_user(user)

        return {
            'user': user,
            'access': str(access),
            'refresh': str(refresh)
        }

# Role Serializer
class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = ['name']

    # Validation to prevent duplicating roles
    def validate(self, data):
        if Role.objects.filter(name=data['name']).exists():
            raise serializers.ValidationError("Role already exists")
        return data

# UserRole Serializer for displaying roles for a user
class UserRoleSerializer(serializers.ModelSerializer):
    role = RoleSerializer(read_only=True)
    
    class Meta:
        model = UserRole
        fields = ['role', 'assigned_at']

# User Profile Serializer
class UserProfileSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer(read_only=True)
    roles = serializers.SerializerMethodField()  # Fetch roles dynamically
    
    class Meta:
        model = UserProfile
        fields = ['user', 'bio', 'profile_pic', 'cover_pic', 'company_name', 'location', 'website', 'specialization', 'roles']

    # Getting all roles assigned to a user (A user can have multiple roles)
    def get_roles(self, obj):
        user_roles = UserRole.objects.filter(user=obj.user)
        return UserRoleSerializer(user_roles, many=True).data
    
    # Updating User Profile
    def update(self, instance, validated_data):
        # Update user profile fields
        for field in ['bio', 'profile_pic', 'cover_pic', 'company_name', 'location', 'website', 'specialization']:
            setattr(instance, field, validated_data.get(field, getattr(instance, field)))
        
        instance.save()

        # Update related CustomUser fields if user data is provided
        user_data = self.context['request'].data.get('user', None)
        if user_data:
            user = instance.user
            user.username = user_data.get('username', user.username)
            user.email = user_data.get('email', user.email)
            user.save()

        return instance
