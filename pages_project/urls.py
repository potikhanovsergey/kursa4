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
from pages.views import PostViewSet, CommentsList, UserViewSet
from sentry_sdk import capture_exception



# Роутеры позволяют быстро и просто сконфигурировать адреса.
router = routers.DefaultRouter()
router.register(r'api/posts', PostViewSet)
router.register(r'api/users', UserViewSet)


# Привяжите конфигурацию URL, используя роутеры.
# Так же мы предоставляем URL для авторизации в браузере.


def trigger_error(request):
  try:
    division_by_zero = 1 / 0
  except Exception as e:
    capture_exception(e)
    division_by_zero = 1 / 0


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('pages.urls')),
    re_path(r'^', include(router.urls)),
    re_path(r'^api/comments', CommentsList.as_view()),
    path('sentry-debug/', trigger_error),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
