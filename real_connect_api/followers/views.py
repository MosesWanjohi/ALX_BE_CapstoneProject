from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from .serializers import FollowerSerializer
from .models import Follower

CustomUser = get_user_model()

# Create your views here.

#Endpoints for follow relationships
class FollowUserView(generics.GenericAPIView):
    serializer_class = FollowerSerializer
    permission_classes = [permissions.IsAuthenticated]


#Follow a user
    def post(self, request, username):
        user_to_follow = get_object_or_404(CustomUser, username=username)
        
        #Ensuring a user cannot follow themselves
        if request.user == user_to_follow:
            raise ValidationError("You cannot follow yourself")
        
        #Creating or checking  if a user is already followed
        follow_instance, created = Follower.objects.get_or_create(
            follower=request.user,
            following=user_to_follow
        )
        if not created:
            raise ValidationError("You are already following this user")
        
        return Response({"message": f"You are now following {user_to_follow.username}"}, status=status.HTTP_201_CREATED)
        
#Unfollow a user
class UnfollowUserView(generics.GenericAPIView):
    serializer_class = FollowerSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    
    def delete(self, request, username):
        user_to_unfollow = get_object_or_404(CustomUser, username=username)
        
        #Checking if a user is being followed before unfollowing
        follow_instance = Follower.objects.filter(follower=request.user, following=user_to_unfollow).first()
        
        if not follow_instance:
            return Response({"message": "You are not following this user"}, status=status.HTTP_404_NOT_FOUND)

        #Unfollowing a user
        follow_instance.delete()
        return Response({"message": f"You have unfollowed {user_to_unfollow.username}"}, status=status.HTTP_200_OK)
