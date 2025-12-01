# chats/middleware.py

from datetime import datetime
from django.http import HttpResponseForbidden


class RestrictAccessByTimeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        current_hour = datetime.now().hour

        # Restrict access OUTSIDE the allowed window (6 PM to 9 PM)
        # Allowed hours: 18, 19, 20, 21
        if current_hour < 18 or current_hour > 21:
            return HttpResponseForbidden("Access to the chat is restricted at this time.")

        return self.get_response(request)

