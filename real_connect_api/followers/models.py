from django.db import models
from accounts.models import CustomUser


# Create your models here.
class Follower(models.Model):
   #User being followed(the one getting the followers)
    user = models.ForeignKey(CustomUser, related_name='followers', on_delete=models.CASCADE)
    #The person following the user
    follower = models.ForeignKey(CustomUser, related_name='following', on_delete=models.CASCADE, null=True, blank=True)
    
    def __str__(self):
        return f"User: {self.user.username} follows {self.follower.username}"
