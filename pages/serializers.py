from rest_framework import serializers
from .models import Post, Comment, Service
from django.contrib.auth.models import User
from datetime import datetime, timedelta, date
from rest_framework.serializers import ValidationError

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['message', 'user_id', 'date', 'post', 'update_date', 'id']  

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['author', 'title', 'description', 'message', 'date', 'img', 'id']
        
    def validate_date(self, date):
        if date < datetime.now().date():
            raise ValidationError('Дата опубликования поста не может быть раньше сегодняшнего дня')
        return date

class UsernameSerializer(serializers.HyperlinkedModelSerializer):
  class Meta:
    model = User
    fields = ['username']

class UserSerializer(serializers.HyperlinkedModelSerializer):
  class Meta:
    model = User
    fields = ['url', 'username', 'email', 'is_staff']
