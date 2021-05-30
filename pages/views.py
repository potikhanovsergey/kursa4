from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.views.generic import TemplateView, ListView, DetailView, CreateView

# Create your views here.
from .models import Post, Comment
from .forms import CommentForm


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
    form = CommentForm

    def post(self, request, *args, **kwargs):
        post = self.get_object()
        form = CommentForm(request.POST)
        if form.is_valid():
            form.instance.post_id = post
            form.instance.post = post
            form.save()

            return redirect(reverse("post_detail", args=[post.id]))

    def get_context_data(self, **kwargs):
        post_comments_count = Comment.objects.all().filter(post_id=self.object.id).count()
        context = super().get_context_data(**kwargs)
        context.update({
            'posts': Post.objects.all(),
            'form': self.form,
            'post_comments_count': post_comments_count
        })
        return context

class BlogCommentCreateView(CreateView):
    model = Comment
    fields = ['author_name', 'message']
    template_name = 'createComment.html'


class ContactsTemplateView(TemplateView):
    template_name = 'contacts.html'
