from django.db import models
from accounts.models import CustomUser


# Create your models here.
class Follower(models.Model):
    user = models.ForeignKey('CustomUser', related_name='following', on_delete=models.CASCADE)
    follower = models.ManyToManyField('self', related_name='user_following', symmetrical=False, blank=True)
    following = models.ManyToManyField('self', related_name='user_followers', symmetrical=False, blank=True)

    #Restricting user to follow only another user only once
    class Meta:
        unique_together = ('user', 'followers')
        

    def __str__(self):
        return f"User: {self.user.username} follows {self.followers.username}"

