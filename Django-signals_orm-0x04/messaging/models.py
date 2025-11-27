from django.db import models
from django.contrib.auth.models import User


class MessageQuerySet(models.QuerySet):
    def unread_for(self, user):
        """Return unread messages for a specific user."""
        return self.filter(receiver=user, read=False).only(
            "id", "sender", "content", "timestamp", "parent_message"
        )


class UnreadMessagesManager(models.Manager):
    def get_queryset(self):
        return MessageQuerySet(self.model, using=self._db)

    def unread_for(self, user):
        """Proxy to QuerySet method."""
        return self.get_queryset().unread_for(user)


class Message(models.Model):
    sender = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="sent_messages"
    )
    receiver = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="received_messages"
    )
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    # Threading (previous task)
    parent_message = models.ForeignKey(
        'self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies'
    )

    # NEW FIELD
    read = models.BooleanField(default=False)

    # MANAGERS
    objects = models.Manager()              # default
    unread = UnreadMessagesManager()         # custom manager

    def __str__(self):
        return f"Message {self.id} from {self.sender}"

