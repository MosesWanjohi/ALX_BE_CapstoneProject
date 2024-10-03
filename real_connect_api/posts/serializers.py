from .models import Post
from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework.exceptions import ValidationError

User = get_user_model()
#Post Serializer
class PostSerializer(serializers.ModelSerializer):
    #Automatically set the author of the post
    author = serializers.HiddenField(default=serializers.CurrentUserDefault())
    author_username = serializers.CharField(source='author.username', read_only=True)
    class Meta:
        model = Post
        fields = [
            'id',
            'author',
            'author_username',
            'title',
            'content',
            'created_at',
            'updated_at',
            'media',
        ]
        read_only_fields = ['author', 'created_at', 'updated_at']


    #Validating the post request for the author field
    def validate(self, data):
        #Check if the current user is the author of the post
        request = self.context['request']
        if 'author' in data and request.user != data['author']:
            raise serializers.ValidationError("You are not the author of this post")
        else:
            return data

    #Validating the post request for content
    def validate_content(self, data):
        #Check if the post contains forbidden words
        forbidden_words = ['forbidden', 'spam', 'scam', 'fraud', 'banned']
        if any(word in data.lower() for word in forbidden_words):
            raise ValidationError("Post contains forbidden words")
        return data
    
