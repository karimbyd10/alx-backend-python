from datetime import datetime, timedelta
from django.http import HttpResponseForbidden


class OffensiveLanguageMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

        # Store IP → list of timestamps of messages
        self.ip_message_log = {}
        self.time_window = timedelta(minutes=1)
        self.message_limit = 5

    def __call__(self, request):
        # Only count POST (sending messages)
        if request.method == "POST":
            ip_address = request.META.get("REMOTE_ADDR", "unknown")
            current_time = datetime.now()

            # Initialize IP record
            if ip_address not in self.ip_message_log:
                self.ip_message_log[ip_address] = []

            # Filter out timestamps older than the time window
            recent_requests = [
                t for t in self.ip_message_log[ip_address]
                if current_time - t < self.time_window
            ]
            self.ip_message_log[ip_address] = recent_requests

            # Check if limit exceeded
            if len(recent_requests) >= self.message_limit:
                return HttpResponseForbidden(
                    "Message rate limit exceeded. Try again later."
                )

            # Record this request as valid
            self.ip_message_log[ip_address].append(current_time)

        return self.get_response(request)

