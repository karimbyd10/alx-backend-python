from django.db.models.signals import post_delete
from django.contrib.auth.models import User
from django.dispatch import receiver

from .models import Message, Notification, MessageHistory


@receiver(post_delete, sender=User)
def cleanup_user_related_data(sender, instance, **kwargs):
    """
    Automatically deletes related records when a User is deleted.
    Runs AFTER the user instance is removed from the database.
    """
    user = instance

    Message.objects.filter(sender=user).delete()
    Message.objects.filter(receiver=user).delete()

    Notification.objects.filter(user=user).delete()

    MessageHistory.objects.filter(user=user).delete()

