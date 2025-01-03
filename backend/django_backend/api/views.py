from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from urllib.parse import urlencode
from django.conf import settings
from django.http import HttpResponseRedirect, JsonResponse
import requests
from rest_framework import status, generics
import json
from api.helpers import get_spotify_token
from api.models import CustomUser, Profile, UserTokens, Comment
from .serializers import ProfileSerializer, CommentSerializer
from .permissions import IsSpotifyAuthenticated

SPOTIFY_API_BASE_URL = "https://api.spotify.com/v1"

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
        print(request.session.items())
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
        url = f"https://api.spotify.com/v1/search?q={query}&type=artist"

        response = requests.get(url, headers=headers)
        print(json.dumps(response.json(), indent=4))

        formatted_artists = [
            {
                "id": artist["uri"].split(":")[-1],
                "name": artist["name"],
                "spotify_url": artist["external_urls"]["spotify"],
                "image_url": artist["images"][0]["url"] if artist["images"] else None,
                "followers": artist["followers"]["total"],
                "genres": artist["genres"],
            }
            for artist in response.json()["artists"]["items"]
        ]

        return JsonResponse({"artists": formatted_artists}, status=200)

class ProfileView(APIView):
    permission_classes = [IsSpotifyAuthenticated]
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
        
class ArtistsView(APIView):
    def get(self, request, artist_id):
        token = get_spotify_token()
        headers = {"Authorization": f"Bearer {token}"}
        url = f"{SPOTIFY_API_BASE_URL}/artists/{artist_id}"
        response = requests.get(url, headers=headers)
        artist = response.json()
        formatted_artist = {
            "id": artist["uri"].split(":")[-1],
            "name": artist["name"],
            "spotify_url": artist["external_urls"]["spotify"],
            "image_url": artist["images"][0]["url"] if artist["images"] else None,
            "followers": artist["followers"]["total"],
            "genres": artist["genres"],
        }

        url_albums = f"{SPOTIFY_API_BASE_URL}/artists/{artist_id}/albums"
        response_albums = requests.get(url_albums, headers=headers)
        albums = response_albums.json()
        formatted_albums = [
            {
                "id": album["id"],
                "name": album["name"],
                "spotify_url": album["external_urls"]["spotify"],
                "image_url": album["images"][0]["url"] if album["images"] else None,
                "release_date": album["release_date"],
            }
            for album in albums["items"]
        ]
        url_top_tracks = f"{SPOTIFY_API_BASE_URL}/artists/{artist_id}/top-tracks"
        response_top_tracks = requests.get(url_top_tracks, headers=headers)
        top_tracks = response_top_tracks.json()
        formatted_tracks = [
            {
                "id": track["id"],
                "name": track["name"],
                "spotify_url": track["external_urls"]["spotify"],
                "image_url": track["album"]["images"][0]["url"] if track["album"]["images"] else None,
            }
            for track in top_tracks["tracks"]
        ]
        
        print(formatted_artist)
        ret = {
            "artist": formatted_artist,
            "albums": formatted_albums,
            "top_tracks": formatted_tracks,
        }
        return Response(ret, status=200)

class CommentListCreateView(APIView):
    serializer_class = CommentSerializer
    #permission_classes = [IsSpotifyAuthenticated]

    def get(self, request):
        artist_id = request.query_params.get('artist_id', '')
        print(artist_id)
        x = Comment.objects.filter(artist_id=artist_id).order_by('-created_at')
        serializer = CommentSerializer(x, many=True)
        return Response(serializer.data)

    def post(self, request):
        data = json.loads(request.body)
        artist_id = data.get('artist_id')
        content = data.get('content')
        if not artist_id or not content:
            return Response({'error': 'Artist ID and content are required.'}, status=status.HTTP_400_BAD_REQUEST)
        
        user = CustomUser.objects.filter(username=request.session.get('username')).first()
        comment = Comment.objects.create(
            artist_id=artist_id,
            user=user,
            content=content
        )

        return Response({
            'id': comment.id,
            'artist_id': comment.artist_id,
            'username': comment.user.username,
            'content': comment.content,
            'created_at': comment.created_at.strftime('%Y-%m-%d %H:%M:%S')
        }, status=status.HTTP_201_CREATED)

class TestView(APIView):
    def get(self, request, user_id):
        url = f"{SPOTIFY_API_BASE_URL}/users/{user_id}/playlists"
        token = get_spotify_token()
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.get(url, headers=headers)
        return JsonResponse(response.json())
