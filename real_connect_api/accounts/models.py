
from django.db import models
from django.contrib.auth.models import AbstractUser


#UserModel
class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=150, unique=True)
    
    followers_count = models.PositiveIntegerField(default=0) 

    def __str__(self):
        return self.username
    
#RoleModel
class Role(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name
  
#UserProfile
class UserProfile(models.Model):
    USER_ROLE_CHOICES = (
        ('agent', 'Agent'),
        ('regular', 'Regular User'),
    )
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(max_length=500, blank=True)
    profile_pic = models.ImageField(upload_to='profile_pics', blank=True, null=True)
    cover_pic = models.ImageField(upload_to='cover_pics', blank=True, null=True)
    company_name = models.CharField(max_length=100, blank=True)
    location = models.CharField(max_length=100, blank=True)
    website = models.URLField(max_length=100, blank=True)
    specialization = models.CharField(max_length=100, blank=True)
    #followers = models.ManyToManyField(CustomUser, related_name='followings', blank=True)
   # following = models.ManyToManyField(CustomUser, related_name='followers', blank=True)

    def __str__(self):
        return f"{self.user.username}'s profile"

#UserRoleModel to link CustomUser and Role
class UserRole(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    assigned_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.role.name}"
    
    class Meta:
        unique_together = ('user', 'role')