from django.db import models
from accounts.models import CustomUser

# Create your models here.

#Post Model
class Post(models.Model):
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    title = models.CharField(max_length=100, blank=False, null=False)
    content = models.TextField(blank=False, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    media = models.ImageField(upload_to="media/", blank=True, null=True)

    def __str__(self):
        return f"Post: {self.title} by {self.author.username}"
