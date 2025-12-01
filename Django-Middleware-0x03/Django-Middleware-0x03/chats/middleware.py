from django.http import HttpResponseForbidden


class RolepermissionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Skip if user is not authenticated
        if not request.user.is_authenticated:
            return HttpResponseForbidden("You must be logged in.")

        # Check if user is admin or moderator
        # Adjust role attribute as per your User model
        # Example assumes `request.user.role` exists
        if getattr(request.user, "role", None) not in ["admin", "moderator"]:
            return HttpResponseForbidden("You do not have permission to perform this action.")

        return self.get_response(request)

