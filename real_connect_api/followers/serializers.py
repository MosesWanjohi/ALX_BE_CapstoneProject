from .models import Follower
from rest_framework import serializers
from django.contrib.auth import get_user_model


User = get_user_model()

#Follower Serializer
class FollowerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Follower
        fields = ['following', 'follower']
  
#validating the follow request
#Ensuring a follower cannot follow themselves
    def validate(self, validated_data):
        if validated_data['follower'] == validated_data['following']:
            raise serializers.ValidationError("You cannot follow yourself!")
        else:
            return validated_data

