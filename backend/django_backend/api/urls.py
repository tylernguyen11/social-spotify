from django.urls import path
from .views import SpotifyLoginView, SpotifyCallbackView, MeView, SearchView, ProfileView

urlpatterns = [
    path('login/', SpotifyLoginView.as_view(), name='spotify-login'),
    path('exchange-code/', SpotifyCallbackView.as_view(), name='spotify-callback'),
    path('me/', MeView.as_view(), name='me'),
    path('search/', SearchView.as_view(), name='search'),
    path('profile/<str:username>/', ProfileView.as_view(), name='profile'),
]
