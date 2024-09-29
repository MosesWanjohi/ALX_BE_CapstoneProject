from .models import Post, Comment, Like
from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework.exceptions import ValidationError

User = get_user_model()
#Post Serializer
class PostSerializer(serializers.ModelSerializer):
    author = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Post
        fields = [
            'id',
            'author',
            'title',
            'content',
            'image',
            'created_at',
            'updated_at',
            'price',
            'location',
            'post_type',
        ]

    #Validating the post request
    def validate(self, data):
        if self.context['request'].user != data['author']:
            raise ValidationError("You are not authorized to perform this action")
        return data

#Comment Serializer
class CommentSerializer(serializers.ModelSerializer):
    author = serializers.HiddenField(default=serializers.CurrentUserDefault())
    post  = serializers.PrimaryKeyRelatedField(queryset=Post.objects.all())

    class Meta:
        model = Comment
        fields = [
            'id',
            'author',
            'post',
            'content',
            'created_at',
            'updated_at',
        ]

    #Validating the comment request
    def validate(self, data):
        if 'forbidden_words' in data.get('content', ''):
            raise ValidationError("Comment contains forbidden words")
        return data


#Like Serializer
class LikeSerializer(serializers.ModelSerializer):
    author = serializers.HiddenField(default=serializers.CurrentUserDefault())
    post  = serializers.PrimaryKeyRelatedField(queryset=Post.objects.all())

    class Meta:
        model = Like
        fields = [
            'id',
            'author',
            'post',
            'created_at',
            'updated_at',
        ]

    #Validating the like request
    def validate(self, data):
        if self.context['request'].user == data['post'].author:
            raise ValidationError("You cannot like your own post")
        
        return data
