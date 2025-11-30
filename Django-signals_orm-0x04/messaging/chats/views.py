# chats/views.py
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_page
from messaging.models import Message, User

# Cache the view for 60 seconds
@cache_page(60)  # cache timeout in seconds
@login_required
def conversation_messages(request, user_id):
    other_user = get_object_or_404(User, pk=user_id)
    # Get messages between logged-in user and other_user
    messages = Message.objects.filter(
        sender__in=[request.user, other_user],
        receiver__in=[request.user, other_user]
    ).order_by("timestamp")
    return render(request, "chats/conversation.html", {"messages": messages, "other_user": other_user})

