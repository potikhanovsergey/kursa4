from django.urls import path, include, re_path
from .views import (HomeTemplateView, AboutTemplateView, BlogTemplateView, ContactsTemplateView, BlogDetailView,
registerPage, loginPage, logoutUser, ServicesTemplateView)

urlpatterns = [
    path('', HomeTemplateView.as_view(), name="home"),
    path('register/', registerPage, name="register"),
    path('login/', loginPage, name="login"),
    path('logout/', logoutUser, name="logout"),
    path('about/', AboutTemplateView.as_view(), name="about"),
    path('blog/', BlogTemplateView.as_view(), name="blog"),
    path('blog/post-<int:pk>/', BlogDetailView.as_view(), name='post_detail'),
    path('contacts/', ContactsTemplateView.as_view(), name="contacts"),
    path('services/', ServicesTemplateView.as_view(), name="services"),
]


