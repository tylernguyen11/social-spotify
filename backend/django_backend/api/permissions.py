from rest_framework.permissions import BasePermission
from api.models import CustomUser

class IsSpotifyAuthenticated(BasePermission):
    """
    Custom permission to check if a valid Spotify access token exists in the session.
    """

    def has_permission(self, request, view):
        access_token = request.session.get('access_token')
        print(access_token)
        if not access_token:
            return False
        return True

        # Verify the token
        """
        # Try refreshing the token if it's expired
        """
