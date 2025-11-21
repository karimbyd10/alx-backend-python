# chats/auth.py
from rest_framework_simplejwt.authentication import JWTAuthentication

class CustomJWTAuthentication(JWTAuthentication):
    """
    Optional custom JWT authentication class.
    Used if additional token validation or user checks are needed.
    """
    pass

