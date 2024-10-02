from .models import Follower
from rest_framework import serializers
from django.contrib.auth import get_user_model


User = get_user_model()

#Follower Serializer
class FollowerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Follower
        fields = ['following', 'follower']
    
    #Method to instantiate Follower
  
        #validating the follow request
        #Ensuring a follower cannot follow themselves
        def validate(self, validated_data):
            if validated_data['follower'] == validated_data['following']:
                raise serializers.ValidationError("You cannot follow yourself!")
            else:
                return serializers.validated_data

        #Creating the Follower object
        def create(self, validated_data):
            return Follower.objects.create(**validated_data)

        #Updating the Follower object
        def update(self, instance, validated_data):
            instance.following = validated_data.get('following', instance.following)
            instance.follower = validated_data.get('follower', instance.follower)
            instance.save()
            return instance


