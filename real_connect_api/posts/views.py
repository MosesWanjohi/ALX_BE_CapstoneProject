from django.shortcuts import get_object_or_404
from .models import Post
from .serializers import PostSerializer
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .permissions import IsAuthorOrReadOnly #Custom permission

# Create your views here.

#Views for handling CRUD operations on posts
class PostViewSet(viewsets.ModelViewSet):
    """
    Only authenticated users can create Posts 
    Only the author of a post can update or delete it.
    Any user can view posts.
    """
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]

#Creating a new post
    def perform_create(self, serializer):
        
        #Set the author of the post to the currently authenticated/logged-in user
        serializer.save(author=self.request.user)

    
#Overriding the perform_create method
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            self.perform_create(serializer)
            return Response({'message': 'Post created successfully', 'post': serializer.data}, status=status.HTTP_201_CREATED)

        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


#Updating a post
    def perform_update(self, serializer):
       
        #Set the author of the post be only one who can update it
        #The author field cannot be changed by the user
        post = serializer.save(author=self.get_object().author)
        return post #Updated post
    
    #Overriding the perform_update method to update an existing post
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()

        #Checking if the user is the author of the post
        if instance.author != self.request.user:
            return Response({'message': 'You are not authorized to update this post'}, status=status.HTTP_403_FORBIDDEN)

        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        if serializer.is_valid():
            self.perform_update(serializer) #Calls the perform_update method
            return Response({'message': 'Post updated successfully', 'post': serializer.data}, status=status.HTTP_200_OK)	
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
#Overriding the perform_destroy method to delete an existing post
#Returns a custom response
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        #Checking if the user is the author of the post
        if instance.author != self.request.user:
            return Response({'message': 'You are not authorized to delete this post'}, status=status.HTTP_403_FORBIDDEN)
        
        self.perform_destroy(instance)
        return Response({'message': 'Post deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
    
    