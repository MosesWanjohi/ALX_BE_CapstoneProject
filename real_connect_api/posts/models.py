from django.db import models
from django.conf import settings

# Create your models here.

#Post Model
class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=100, blank=False, null=False)
    content = models.TextField(blank=False, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    media = models.ImageField(upload_to="media/", blank=True, null=True)

    def __str__(self):
        return f"Post: {self.title} by {self.author.username}"

#Implementing Likes and Comments For Posts

#Like Model
class Like(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    """
        A user can only like a post once
    """
    class Meta:
        unique_together = ('author', 'post')

    def __str__(self):

        return f"{self.author.username} liked {self.post.title}"
    

#Comment Model
class Comment(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Comment: {self.content} by {self.author.username}"
