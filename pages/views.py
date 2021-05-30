from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.views.generic import TemplateView, ListView, DetailView
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
# Create your views here.
from django.conf import settings
from .models import Post, Comment
from django.utils import dateformat, timezone
from .forms import CommentForm, CreateUserForm, UpdateForm

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
    update_form = UpdateForm
    def post(self, request, *args, **kwargs):
        post = self.get_object()
        if request.method == 'POST' and 'send' in request.POST:
            try:
                form = CommentForm(request.POST)
                if form.is_valid():
                    form.instance.post_id = post
                    if (request.user.is_authenticated):
                        form.instance.user = request.user
                    else:
                        form.instance.user = User.objects.all().get(username="Гость")
                    form.save()
                    messages.success(request, 'Вы успешно добавили комментарий!')
                if (request.POST['message'].strip() == ''):
                    messages.warning(request, 'Комментарий не может быть пустым')
                return redirect(reverse("post_detail", args=[post.id]))
            except:
                messages.warning(request, 'Что-то пошло не так')
                return redirect(reverse("post_detail", args=[post.id]))

        elif request.method == 'POST' and 'delete' in request.POST:
            id = request.POST['comment_id']
            comment = get_object_or_404(Comment, id=id)
            try:
                comment.delete()
                messages.success(request, 'Вы успешно удалили комментарий!')
            except:
                messages.warning(request, 'Что-то пошло не так')
            return redirect(reverse('post_detail', args=[post.id]))
        elif request.method == 'POST' and 'update' in request.POST:
            id = request.POST['edit-comment_id']
            message = request.POST['message']
            comment = get_object_or_404(Comment, id=id)
            if (message.strip() == ''):
                messages.warning(request, 'Комментарий не может быть пустым')
                return redirect(reverse('post_detail', args=[post.id]))
            try:
                comment.message = message
                comment.update_date = timezone.now()
                comment.save()
                messages.success(request, 'Вы успешно отредактировали комментарий!')
            except:
                messages.error(request, 'Что-то пошло не так :с')


            return redirect(reverse('post_detail', args=[post.id]))

    def get_context_data(self, **kwargs):
        post_comments_count = Comment.objects.all().filter(post_id=self.object.id).count()
        context = super().get_context_data(**kwargs)
        context.update({
            'posts': Post.objects.all(),
            'form': self.form,
            'updateForm': self.update_form,
            'post_comments_count': post_comments_count
        })
        return context




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



