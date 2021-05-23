from django.shortcuts import render
from django.views.generic import TemplateView, ListView, DetailView
# Create your views here.
from .models import Post

class HomeTemplateView(TemplateView):
    template_name = 'kursovaya/index.html'

class AboutTemplateView(TemplateView):
    template_name = 'kursovaya/about.html'

class BlogTemplateView(ListView):
    model = Post
    template_name = 'kursovaya/blog.html'
    context_object_name = 'posts'

class BlogDetailView(DetailView):
    model = Post
    template_name = 'kursovaya/post_detail.html'

class ContactsTemplateView(TemplateView):
    template_name = 'kursovaya/contacts.html'



