from django.db import models
from accounts.models import CustomUser


# Create your models here.
#Post Model
class Post(models.Model):
    POST_TYPES_CHOICES = (
        ("listing", "Listing"),
        ("event", "Event"),
        ("blog post", "Blog Post"),
        ("market analysis", "Market Analysis"),
    )
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    title = models.CharField(max_length=100, blank=False, null=False)
    content = models.TextField(blank=False, null=False)
    created_at = models.DateTimeField(auto_now_add=True, )
    updated_at = models.DateTimeField(auto_now=True)
    media = models.ImageField(upload_to="media", blank=True, null=True)
    price = models.DecimalField(max_digits=10, default=0, decimal_places=2, blank=True, null=True)
    location = models.CharField(max_length=100, blank=True, null=True)
    post_type = models.CharField(max_length=100, choices=POST_TYPES_CHOICES, default="listing", blank=False, null=False)

    def __str__(self):
        return f"Post: {self.title} by {self.author.username}"

#Implementing functionality on posts
#Commenting on posts
class Comment(models.Model):
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    content = models.TextField(blank=False, null=False)
    created_at = models.DateTimeField(auto_now_add=True, )
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.author.username}Commented on {self.content}"

#Likes on posts
class Like(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True, )
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.author.username} liked {self.post.title}"