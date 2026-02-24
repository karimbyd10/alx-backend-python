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


class IsConversationParticipant(permissions.BasePermission):
    """
    Allow only participants of a conversation to:
    - view messages (GET)
    - send messages (POST)
    - update messages (PUT/PATCH)
    - delete messages (DELETE)
    """

    def has_permission(self, request, view):
        """
        For POST (creating message), check conversation from request data.
        """
        if request.method == "POST":
            conversation = view.get_conversation_from_request(request)
            if conversation:
                return request.user in conversation.participants.all()
            return False

        # For other methods, allow permission check to continue
        return True

    def has_object_permission(self, request, view, obj):
        """
        For GET, PUT, PATCH, DELETE — check object-level permission.
        """
        if request.method in ["GET", "PUT", "PATCH", "DELETE"]:
            return request.user in obj.conversation.participants.all()

        return False