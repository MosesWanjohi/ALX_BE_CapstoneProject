#Signals to keep track of followers count
from django.apps import AppConfig
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Follower
from notifications.models import Notification
from django.contrib.contenttypes.models import ContentType

@receiver(post_save, sender=Follower)
def increment_follower_count(sender, instance, created, **kwargs):
    """
    Signal receiver to increment followers count of the following user
    whenever a new follow relationship is created.
    """
    if created:
        instance.following.followers_count += 1
        instance.following.save(update_fields=['followers_count'])
    
    #Incrementing following count for the user doing the following
        instance.follower.following_count += 1
        instance.follower.save(update_fields=['following_count'])

    #Creating a notification for the user being followed
    Notification.objects.create(
        recipient = instance.following, #The user being followed
        actor = instance.following, #The user doing the following
        verb = "started following",
        content_type = ContentType.objects.get_for_model(Follower),
        object_id = instance.id #The id of the follow relationship
    )



@receiver(post_delete, sender=Follower)
def decrement_follower_count(sender, instance, **kwargs):
    """
    Signal receiver to decrement both followers count of the following user
    and following count of the follower user whenever a follow relationship is deleted.
    """
    if instance.following.followers_count > 0:
        instance.following.followers_count -= 1
        instance.following.save(update_fields=['followers_count'])


    #Decrementing following count for the user doing the unfollowing
    if instance.follower.following_count > 0:
        instance.follower.following_count -= 1
        instance.follower.save(update_fields=['following_count'])