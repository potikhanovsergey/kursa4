from django.shortcuts import render, get_object_or_404
from django.views.generic import TemplateView, ListView, DetailView, CreateView

# Create your views here.
from .models import Post, Comment



class HomeTemplateView(TemplateView):
    template_name = 'index.html'

class AboutTemplateView(TemplateView):
    template_name = 'about.html'

class BlogTemplateView(ListView):
    model = Post
    template_name = 'blog.html'
    context_object_name = 'posts'

class BlogDetailView(DetailView):
    model = Post
    template_name = 'post_detail.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['posts'] = Post.objects.all()
        return context

class BlogCommentCreateView(CreateView):
    model = Comment
    fields = ['author_name', 'message']
    template_name = 'createComment.html'


class ContactsTemplateView(TemplateView):
    template_name = 'contacts.html'
