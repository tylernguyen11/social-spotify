from rest_framework import serializers
from api.models import Profile

class ProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    class Meta:
        model = Profile
        fields = ['username', 'display_name', 'profile_picture', 'bio', 'followers', 'following'] 
