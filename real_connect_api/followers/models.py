from django.db import models
from django.contrib.auth import get_user_model

CustomUser = get_user_model()

# Create your models here.
class Follower(models.Model):
   #User being followed(the one getting the followers)
    following = models.ForeignKey(CustomUser, related_name='followers', on_delete=models.CASCADE)

    #The person following the user
    follower = models.ForeignKey(CustomUser, related_name='following', on_delete=models.CASCADE)
    
    #The time the follow relationship was created
    created_at = models.DateTimeField(auto_now_add=True)
    
    #Ensuring a follower can only follow a user once
    class Meta:
        unique_together = ('follower', 'following')
    
    def __str__(self):
        return f"User: {self.follower.username} follows {self.following.username}"

    def save(self, *args, **kwargs):
        if self.follower == self.following:
            raise ValueError("You cannot follow yourself")
        
        #Updating the follower count of the following user if the follow relationship is created
        if not Follower.objects.filter(follower=self.follower, following=self.following).exists():
            self.following.followers_count += 1
            self.following.save()
        
        super().save(*args, **kwargs)
    
    def delete(self, *args, **kwargs):
        #Updating the follower count of the following user if the follow relationship is deleted
        self.following.followers_count -= 1
        self.following.save()
        
        super().delete(*args, **kwargs)
        
