from rest_framework import permissions

class IsOwnerOfConversation(permissions.BasePermission):
    """
    Allows access only to users who are participants of the conversation.
    """

    def has_object_permission(self, request, view, obj):
        return request.user in obj.participants.all()


class IsSenderOfMessage(permissions.BasePermission):
    """
    Allows access only to the sender of the message.
    """

    def has_object_permission(self, request, view, obj):
        return obj.sender == request.user