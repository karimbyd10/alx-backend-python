# chats/middleware.py

from datetime import datetime

class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.log_file = "requests.log"

    def __call__(self, request):
        # Get username or Anonymous
        user = request.user.username if request.user.is_authenticated else "Anonymous"

        # Log format
        log_entry = f"{datetime.now()} - User: {user} - Path: {request.path}\n"

        # Write to requests.log
        with open(self.log_file, "a") as file:
            file.write(log_entry)

        response = self.get_response(request)
        return response

