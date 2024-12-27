import time
import requests
from base64 import b64encode
from django.core.management.base import BaseCommand
from django.conf import settings

class Command(BaseCommand):
    help = 'Fetch Spotify App Token'
    def handle(self, *args, **kwargs):
        from api.models import SpotifyToken

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
        self.stdout.write(self.style.SUCCESS('Token fetched and saved!' + token_data['access_token']))
