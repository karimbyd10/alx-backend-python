# messaging_app/chats/urls.py
from django.urls import path, include
from rest_framework import routers
from .views import ConversationViewSet, MessageViewSet

# ----------------------------
# DRF router using DefaultRouter()
# ----------------------------
router = routers.DefaultRouter()
router.register(r'conversations', ConversationViewSet, basename='conversation')
router.register(r'messages', MessageViewSet, basename='message')

urlpatterns = [
    path('', include(router.urls)),
    path('api/', include('chats.urls')),  # <-- This registers the chats API under /api/
]