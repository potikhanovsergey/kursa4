"""pages_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.response import Response
import django_filters
from rest_framework import routers, serializers, viewsets, status, generics, pagination
from rest_framework.decorators import action
from pages.models import Post, Comment
from django.contrib.auth.models import User
import json
from datetime import datetime, timedelta, date
from pages.serializers import UserSerializer, UsernameSerializer
from django.db.models import Q
from pages.views import PostViewSet, CommentsList


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    action_serializers = {
        'change_username': UsernameSerializer,
    }

    @action(detail=True, methods=['post'])
    def change_username(self, request, pk=None):
        user = self.get_object()
        serializer = UsernameSerializer(data=request.data)
        if (serializer.is_valid()):
          username = serializer.validated_data['username']
          user.username = username
          user.save()
          return Response({'status': 'Username changed'})
        else:
          return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)

    def get_serializer_class(self):
        if hasattr(self, 'action_serializers'):
            return self.action_serializers.get(self.action, self.serializer_class)

        return super(MyModelViewSet, self).get_serializer_class()



# Роутеры позволяют быстро и просто сконфигурировать адреса.
router = routers.DefaultRouter()
router.register(r'api-auth/posts', PostViewSet)
router.register(r'api-auth/users', UserViewSet)


# Привяжите конфигурацию URL, используя роутеры.
# Так же мы предоставляем URL для авторизации в браузере.

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('pages.urls')),
    re_path(r'^', include(router.urls)),
    re_path(r'^api-auth/comments', CommentsList.as_view())
]


urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
