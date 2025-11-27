from django.views.decorators.cache import cache_page
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required

from .models import Conversation, Message
from django.http import JsonResponse


@cache_page(60)   # Cache for 60 seconds
@login_required
def conversation_messages(request, conversation_id):
    conversation = get_object_or_404(Conversation, id=conversation_id)

    # Ensure logged-in user is a participant
    if request.user not in conversation.participants.all():
        return JsonResponse({"error": "Not allowed"}, status=403)

    messages = Message.objects.filter(conversation=conversation).select_related(
        "sender"
    )

    data = [
        {
            "id": msg.id,
            "sender": msg.sender.username,
            "content": msg.content,
            "timestamp": msg.timestamp.isoformat(),
        }
        for msg in messages
    ]

    return JsonResponse({"messages": data}, status=200)

