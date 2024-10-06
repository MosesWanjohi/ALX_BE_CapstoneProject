from django.shortcuts import get_object_or_404
from .models import Post, Like, Comment
from notifications.models import Notification
from .serializers import PostSerializer, LikeSerializer, CommentSerializer
from rest_framework import filters
from rest_framework import generics,viewsets, status
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from .permissions import IsAuthorOrReadOnly #Custom permission
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone
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
    
#Feed of posts Endpoint
class FeedView(ListAPIView):
    """
    Endpoint for retrieving posts from the user's following
    """
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]
    queryset = Post.objects.all()

    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    filter_fields = ['author__username']
    search_fields = ['title', 'content']
    ordering_fields = ['-created_at']
    ordering = ['-created_at'] #Order by created_at in descending order

    def get_queryset(self):
        user = self.request.user
        #Fetching all users the current user is following
        following_users = user.following.values_list('following', flat=True)
        
        #Overriding the get_queryset method to filter feed posts by date created 

        queryset = Post.objects.filter(author__id__in=following_users)

        #Filter posts by date range if provided
        date_from = self.request.query_params.get('date_from')
        date_to = self.request.query_params.get('date_to')

        if date_from:
            queryset = queryset.filter(created_at__gte=date_from)
        
        if date_to:
            queryset = queryset.filter(created_at__lte=date_to)

        return queryset.order_by('-created_at')

#Endpoints for Likes and Comments

#Liks Endpoint
class LikePostView(generics.GenericAPIView):
    serializer_class = LikeSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, pk, *args, **kwargs):
        post = get_object_or_404(Post, pk=pk)

        #Using get_or_create to check if the user has already liked the post
        like, created = Like.objects.get_or_create(user=request.user, post=post)

        if created:
            """
            If the user has not liked the post
            Create a new like instance.
            Also send a notification to the author of the post about the new like
            """
            Notification.objects.create(
                recipient = post.author,
                actor = request.user,
                verb = "liked",
                content_type = ContentType.objects.get_for_model(Post),
                object_id = post.id
            )
            return Response({'message': 'Post liked'}, status=status.HTTP_200_CREATED)
        else:
            #Unliking the post if the user has already liked it.
            like.delete()
            return Response({'message': 'Post unliked'}, status=status.HTTP_200_OK)
        

#Comments Endpoint
class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, pk, *args, **kwargs):
        post = get_object_or_404(Post, pk=pk)
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=self.request.user, post=post)
            
            Notification.objects.create(
                recipient = post.author,
                actor = request.user,
                verb = "commented",
                content_type = ContentType.objects.get_for_model(Post),
                object_id = post.id
            )
            return Response({'message': 'Comment created successfully', 'comment': serializer.data}, status=status.HTTP_201_CREATED)

        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def list(self, request, pk, *args, **kwargs):
        post = get_object_or_404(Post, pk=pk)

        #Fetching all the comments for a specific post
        queryset = self.get_queryset().filter(post=post)
        serializer = self.get_serializer(queryset, many=True)
        return Response({'comments': serializer.data}, status=status.HTTP_200_OK)
    
    def retrieve(self, request, *args, **kwargs):
        comment = self.get_object()
        serializer = self.get_serializer(comment)
        return Response({'comment': serializer.data}, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        """
        Updating a comment endpoint
        ---
        # noqa: E501
        """
        instance = self.get_object()

        #Ensuring only the author of the comment can update it
        if instance.user != self.request.user:
            return Response({'message': 'You are not authorized to update this comment'}, status=status.HTTP_403_FORBIDDEN)
        
        partial = kwargs.pop('partial', False)
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        if serializer.is_valid():
            self.perform_update(serializer)
            return Response({'message': 'Comment updated successfully', 'comment': serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        
        #Only the author of the comment can delete it
        if instance.user != self.request.user:
            return Response({'message': 'You are not authorized to delete this comment'}, status=status.HTTP_403_FORBIDDEN)
        self.perform_destroy(instance)
        return Response({'message': 'Comment deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
    
