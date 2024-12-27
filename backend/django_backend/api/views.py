from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from urllib.parse import urlencode
from django.conf import settings
from django.http import HttpResponseRedirect, JsonResponse
import requests
from rest_framework import status
import json
from api.helpers import get_spotify_token
from api.models import CustomUser, Profile, UserTokens
from .serializers import ProfileSerializer

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
        return JsonResponse({'url': url})

class SpotifyCallbackView(APIView):
    def post(self, request):
        data = json.loads(request.body)
        code = data['code']
        error = request.GET.get('error')
        if error:
            return Response({'error': error}, status=status.HTTP_400_BAD_REQUEST)

        # Exchange the code for an access token
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
            print("Token exchange failed:", response.status_code, response.text)
            return Response({'error': response.json()}, status=response.status_code)
        token_data = response.json()
        print(token_data.items())
        access_token = token_data.get('access_token')
        spotify_user_data = self.get_spotify_user_info(access_token)
        user_id = spotify_user_data.get('id')

        if not user_id:
            return Response({'error': 'Failed to fetch user data'}, status=400)
        request.session['access_token'] = access_token
        request.session['username'] = user_id
        request.session.modified = True
        request.session.save()

        user = CustomUser.objects.filter(username=user_id).first()
        # Create User and Profile
        if not user:
            try:
                user = CustomUser.objects.create_user(
                    username=user_id, email=spotify_user_data.get('email'), country=spotify_user_data.get('country')
                )
                Profile.objects.create(user=user, display_name=spotify_user_data.get('display_name'), bio="I am a music lover")
            except:
                print("Something went wrong")
        UserTokens.objects.update_or_create(user=user, defaults={'refresh_token': token_data.get('refresh_token')})
        return JsonResponse({'message': 'Successfully logged in', 'username': user_id})
    
    def get_spotify_user_info(self, access_token):
        url = "https://api.spotify.com/v1/me"
        headers = {'Authorization': f'Bearer {access_token}'}
        response = requests.get(url, headers=headers)
        return response.json()

    
class LogoutView(APIView):
    def post(self, request):
        request.session.flush()
        return JsonResponse({'message': 'Successfully logged out'})
    
class MeView(APIView):
    def get(self, request):
        access_token = request.session.get('access_token')
        print(access_token)
        headers = {'Authorization': f'Bearer {access_token}'}
        url = 'https://api.spotify.com/v1/me'
        res = requests.get(url, headers=headers)
        return JsonResponse(res.json())
    
class SearchView(APIView):
    def get(self, request):
        query = request.query_params.get('q', '')
        if not query:
            return Response({'error': 'Query parameter "q" is required'}, status=400)

        token = get_spotify_token()
        headers = {"Authorization": f"Bearer {token}"}
        url = f"https://api.spotify.com/v1/search?q={query}&type=track"

        response = requests.get(url, headers=headers)
        return Response(response.json())

class ProfileView(APIView):
    def get(self, request, username):
        if not username:
            return Response({'error': 'Username not provided'}, status=400)
        try:
            profile = Profile.objects.get(user__username=username)
            serializer = ProfileSerializer(profile)
            print(serializer.data)
            return Response(serializer.data)
        except Profile.DoesNotExist:
            return Response({'error': 'Profile not found'}, status=404)