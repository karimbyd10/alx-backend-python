from datetime import datetime
from django.http import HttpResponseForbidden

class RestrictAccessByTimeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        current_hour = datetime.now().hour
        
        # Allow access only between 18:00 (6 PM) and 21:59 (9 PM)
        if current_hour < 18 or current_hour > 21:
            return HttpResponseForbidden("Access to the chat is restricted at this time.")
        
        return self.get_response(request)

