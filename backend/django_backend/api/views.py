from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from urllib.parse import urlencode
from django.conf import settings
from django.http import HttpResponseRedirect
import requests
from rest_framework import status

class SpotifyLoginView(APIView):
    def get(self, request):
        scopes = 'user-read-private user-read-email'
        query_params = urlencode({
            'client_id': settings.SPOTIFY_CLIENT_ID,
            'response_type': 'code',
            'redirect_uri': settings.SPOTIFY_REDIRECT_URI,
            'scope': scopes,
        })
        url = f"https://accounts.spotify.com/authorize?{query_params}"
        return HttpResponseRedirect(url)
    
class SpotifyCallbackView(APIView):
    def get(self, request):
        code = request.GET.get('code')
        error = request.GET.get('error')

        if error:
            return Response({'error': error}, status=status.HTTP_400_BAD_REQUEST)

        token_url = "https://accounts.spotify.com/api/token"
        payload = {
            'grant_type': 'authorization_code',
            'code': code,
            'redirect_uri': settings.SPOTIFY_REDIRECT_URI,
            'client_id': settings.SPOTIFY_CLIENT_ID,
            'client_secret': settings.SPOTIFY_CLIENT_SECRET,
        }
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}

        response = requests.post(token_url, data=payload, headers=headers)
        if response.status_code != 200:
            return Response({'error': 'Failed to fetch access token'}, status=status.HTTP_400_BAD_REQUEST)
        token_data = response.json()
        access_token = token_data.get('access_token')
        user_profile = self.fetch_spotify_user_profile(access_token)

        return Response(user_profile)

    def fetch_spotify_user_profile(self, access_token):
        url = "https://api.spotify.com/v1/me"
        headers = {'Authorization': f'Bearer {access_token}'}
        response = requests.get(url, headers=headers)
        return response.json()
