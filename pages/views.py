from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.views.generic import TemplateView, ListView, DetailView, CreateView
from django.contrib.auth import authenticate, login, logout


from django.contrib import messages

# Create your views here.
from .models import Post, Comment
from .forms import CommentForm, CreateUserForm

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

def registerPage(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        form = CreateUserForm()
        if request.method == 'POST':
            form = CreateUserForm(request.POST)
            if form.is_valid():
                form.save()
                user = form.cleaned_data.get('username')

                messages.success(request, '{0}, вы успешно зарегистрировались!'.format(user))

                return redirect('login')

        context = {'form': form}
        return render(request, 'register.html', context)

def loginPage(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)

            if (user is not None):
                login(request, user)
                return redirect('home')
            else:
                messages.info(request, 'Никнейм или пароль введены неверно')

        context = {}
        return render(request, 'login.html', context)

def logoutUser(request):
    logout(request)
    return redirect('login')

class ContactsTemplateView(TemplateView):
    template_name = 'contacts.html'
