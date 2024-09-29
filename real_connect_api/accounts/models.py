
from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=150, unique=True)
    bio = models.TextField(max_length=500, blank=True)
    profile_pic = models.ImageField(upload_to='profile_pics', blank=True, null=True)
    location = models.CharField(max_length=100, blank=True)
    website = models.CharField(max_length=100, blank=True)
    cover_pic = models.ImageField(upload_to='cover_pics', blank=True, null=True)

    def __str__(self):
        return self.username
    
#UserProfile
class UserProfile(models.Model):
    USER_ROLE_CHOICES = (
        ('agent', 'Agent'),
        ('regular', 'Regular User'),
    )

    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='profile')
    role = models.CharField(max_length=10, choices=USER_ROLE_CHOICES, default="regular")

    def __str__(self):
        return f"{self.user.username}'s profile"
