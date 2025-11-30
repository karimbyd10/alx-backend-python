# messaging/views.py
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_cookie
from .models import Message, User

# Cache the view for 60 seconds
@cache_page(60)  # ✅ 60-second cache timeout
@vary_on_cookie     # ensures caching respects the logged-in user
@login_required
def conversation_messages(request, user_id):
    other_user = get_object_or_404(User, pk=user_id)
    messages = Message.objects.filter(
        sender__in=[request.user, other_user],
        receiver__in=[request.user, other_user]
    ).order_by("timestamp")
    return render(request, "messaging/conversation.html", {
        "messages": messages,
        "other_user": other_user
    })

