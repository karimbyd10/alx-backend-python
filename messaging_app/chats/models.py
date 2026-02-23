# messaging_app/chats/models.py
import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser

# ----------------------------
# Custom User Model
# ----------------------------
class User(AbstractUser):
    USER_ROLES = (
        ('guest', 'Guest'),
        ('host', 'Host'),
        ('admin', 'Admin'),
    )

    # Override default ID to UUID
    user_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    
    # Required fields
    first_name = models.CharField(max_length=150, null=False)
    last_name = models.CharField(max_length=150, null=False)
    email = models.EmailField(unique=True, null=False)
    password_hash = models.CharField(max_length=128, null=False)
    
    # Optional fields
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    
    # Role
    role = models.CharField(max_length=10, choices=USER_ROLES, default='guest', null=False)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)

    # Username and email configuration
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.email})"


# ----------------------------
# Conversation Model
# ----------------------------
class Conversation(models.Model):
    conversation_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    participants = models.ManyToManyField(User, related_name='conversations')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Conversation {self.conversation_id}"


# ----------------------------
# Message Model
# ----------------------------
class Message(models.Model):
    message_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='messages')
    message_body = models.TextField(null=False)
    sent_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message {self.message_id} from {self.sender.email}"