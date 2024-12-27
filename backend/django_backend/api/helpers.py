import time
import requests
from base64 import b64encode
from api.models import SpotifyToken
from django.conf import settings

def get_spotify_token():
    """
    Returns a valid Spotify access token.
    If the current token is expired, it refreshes it.
    """
    token = SpotifyToken.objects.first()
    if not token or token.expires_in <= time.time():
        refresh_spotify_token()
    return SpotifyToken.objects.first().access_token

def refresh_spotify_token():
    """
    Fetches a new Spotify access token using the client credentials flow
    and updates the stored token in the database.
    """
    client_id = settings.SPOTIFY_CLIENT_ID
    client_secret = settings.SPOTIFY_CLIENT_SECRET
    token_url = 'https://accounts.spotify.com/api/token'

    auth_header = b64encode(f"{client_id}:{client_secret}".encode()).decode()
    headers = {"Authorization": f"Basic {auth_header}"}
    payload = {"grant_type": "client_credentials"}

    response = requests.post(token_url, data=payload, headers=headers)
    response.raise_for_status()
    token_data = response.json()

    SpotifyToken.objects.update_or_create(
        id=1, 
        defaults={
            'access_token': token_data['access_token'],
            'expires_in': time.time() + token_data['expires_in'],
        }
    )
