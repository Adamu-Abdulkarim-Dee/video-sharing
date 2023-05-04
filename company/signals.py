from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Profile, Notification, Comment
from django.urls import reverse

User = settings.AUTH_USER_MODEL

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=Comment)
def comment_post_save(sender, instance, **kwargs):
    user = instance.post.user
    message = f'"{instance.user} commented on your {instance.post.title}"'
    link = reverse('Play-Video', args={str(instance.post.slug)})
    notification = Notification(user=user, message=message, link=link)
    notification.save()


