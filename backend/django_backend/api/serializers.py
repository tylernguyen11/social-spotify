from rest_framework import serializers
from api.models import Profile, Comment

class ProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    class Meta:
        model = Profile
        fields = ['username', 'display_name', 'profile_picture', 'bio', 'followers', 'following'] 

class CommentSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    def create(self, validated_data):
        return Comment(**validated_data)
    class Meta:
        model = Comment
        fields = ['id', 'artist_id', 'username', 'content', 'created_at']
        read_only_fields = ['id', 'created_at']
