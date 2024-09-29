from .models import Follower
from rest_framework import serializers

#Follower Serializer
class FollowerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Follower
        fields = '__all__'
    
    #Method to instantiate Follower
    def create(self, validated_data):
        #validating the follow request
        #Ensuring a follower cannot follow themselves
        if validated_data['user'] == validated_data['follower']:
            raise serializers.ValidationError("You cannot follow yourself!")
        
        #Ensuring a follower can only follow a user once (they already follow that user
        if Follower.objects.filter(user=validated_data['user'], follower=validated_data['follower']).exists():
            raise serializers.ValidationError("You already followed this user!")
        
        #Creating the Follower object
        return Follower.objects.create(**validated_data)


