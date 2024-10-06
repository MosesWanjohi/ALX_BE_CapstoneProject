from django.db import models
from django.conf import settings

# Create your models here.
class Follower(models.Model):
   #User being followed(the one getting the followers)
    following = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='followers', on_delete=models.CASCADE)

    #The person following the user
    follower = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='following', on_delete=models.CASCADE)
    
    #The time the follow relationship was created
    created_at = models.DateTimeField(auto_now_add=True)
    
    #Ensuring a follower can only follow a user once
    class Meta:
        unique_together = ('follower', 'following')
    
    def __str__(self):
        return f"User: {self.follower.username} follows {self.following.username}"
    