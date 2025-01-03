from django.contrib import admin
from .models import CustomUser, Comment

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    pass

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('artist_id', 'user', 'content', 'created_at')
