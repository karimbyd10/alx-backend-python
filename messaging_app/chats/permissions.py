from rest_framework import permissions

class IsAuthenticatedAndOwner(permissions.BasePermission):
    """
    Allows access only to authenticated users who own the object.
    """

    def has_object_permission(self, request, view, obj):
        return (
            request.user and
            request.user.is_authenticated and
            obj.sender == request.user
        )