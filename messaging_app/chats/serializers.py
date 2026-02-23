# messaging_app/chats/serializers.py
from rest_framework import serializers
from .models import User, Conversation, Message

# ----------------------------
# User Serializer
# ----------------------------
class UserSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()  # Custom field

    class Meta:
        model = User
        fields = [
            'user_id',
            'first_name',
            'last_name',
            'full_name',
            'email',
            'phone_number',
            'role',
            'created_at'
        ]
        read_only_fields = ['user_id', 'created_at']

    def get_full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"


# ----------------------------
# Message Serializer
# ----------------------------
class MessageSerializer(serializers.ModelSerializer):
    sender_email = serializers.CharField(source='sender.email', read_only=True)
    sender_name = serializers.SerializerMethodField()

    class Meta:
        model = Message
        fields = ['message_id', 'sender', 'sender_email', 'sender_name', 'message_body', 'sent_at']
        read_only_fields = ['message_id', 'sent_at', 'sender_email', 'sender_name']

    def get_sender_name(self, obj):
        return f"{obj.sender.first_name} {obj.sender.last_name}"


# ----------------------------
# Conversation Serializer
# ----------------------------
class ConversationSerializer(serializers.ModelSerializer):
    participants = UserSerializer(many=True, read_only=True)
    messages = serializers.SerializerMethodField()

    class Meta:
        model = Conversation
        fields = ['conversation_id', 'participants', 'messages', 'created_at']
        read_only_fields = ['conversation_id', 'created_at']

    def get_messages(self, obj):
        # Include messages sorted by sent_at
        messages = obj.messages.order_by('sent_at')
        return MessageSerializer(messages, many=True).data

    # Example of validation: ensure at least 2 participants
    def validate(self, data):
        participants = self.instance.participants.all() if self.instance else data.get('participants', [])
        if len(participants) < 2:
            raise serializers.ValidationError("A conversation must have at least 2 participants.")
        return data