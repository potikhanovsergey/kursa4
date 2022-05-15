from rest_framework import serializers
from .models import Post, Comment, Service
from django.contrib.auth.models import User

class CommentSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Comment
        fields = ['user', 'message', 'date']

class PostSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Post
        fields = ['author', 'title', 'description', 'message', 'date']
        
    def validate_date(self, date):
        if date < datetime.now().date():
            raise ValidationError('Дата опубликования поста не может быть меньше текущего времени')
        return date

class UsernameSerializer(serializers.HyperlinkedModelSerializer):
  class Meta:
    model = User
    fields = ['username']

class UserSerializer(serializers.HyperlinkedModelSerializer):
  class Meta:
    model = User
    fields = ['url', 'username', 'email', 'is_staff']