from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.views.generic import TemplateView, ListView, DetailView
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
# Create your views here.
from rest_framework import routers, serializers, viewsets, status, generics, pagination
from django.conf import settings
from .models import Post, Comment, Service
from django.utils import dateformat, timezone
from .forms import CommentForm, CreateUserForm, UpdateForm
from .serializers import PostSerializer, CommentSerializer, UserSerializer, UsernameSerializer
from rest_framework.decorators import action
from django.db.models import Q
from datetime import datetime, timedelta, date
from rest_framework.response import Response

from django.core import serializers
from django.forms.models import model_to_dict
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

class StandardResultsSetPagination(pagination.PageNumberPagination):
    page_size = 6
    page_size_query_param = 'page_size'
    max_page_size = 1000

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

class ServicesTemplateView(ListView):
    model = Service
    context_object_name = 'services'
    template_name = 'services.html'

@method_decorator(csrf_exempt, name='dispatch')
class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    pagination_class = None
    authentication_classes = []
    permission_classes = ()

    action_serializers = {
        'new_comment': CommentSerializer,
    }

    @action(methods=['GET'], detail=False)
    def get_authors(self, request, **kwargs):
        authors = Post.objects.values_list('author', flat=True)
        authors = set(authors)
        return Response(authors)
    
    @action(methods=['GET'], detail=True)
    def comments(self, request, **kwargs):
      post = self.get_object()
      comments = Comment.objects.filter(post=post).values()
      return Response(comments)

    @action(detail=True, methods=['POST'])
    def new_comment(self, request, pk=None):
      serializer = CommentSerializer(data=request.data)
      if (serializer.is_valid()):
        serializer.save()
        id = serializer.data['id']
        return Response(id)
      else:
        return Response(serializer.errors,
          status=status.HTTP_400_BAD_REQUEST)
    
    @action(methods=['DELETE'], detail=False)
    def delete_today_posts(self, request, **kwargs):
      posts = Post.objects.filter(Q(date=date.today()))
      return Response(posts.delete())
      
    @action(methods=['DELETE'], detail=False)
    def delete_starts_with(self, request, **kwargs):
      posts = Post.objects.filter(Q(title__startswith="31"))
      return Response(posts.delete())

    def get_serializer_class(self):
      if hasattr(self, 'action_serializers'):
          return self.action_serializers.get(self.action, self.serializer_class)

      return super(MyModelViewSet, self).get_serializer_class()

@method_decorator(csrf_exempt, name='dispatch')
class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    pagination_class = None
    authentication_classes = []
    permission_classes = ()

    def delete(self, request, pk, format=None):
      comment = self.get_object(pk)
      return Response(1)
    
    def update(self, request, *args, **kwargs):
      instance = self.get_object()
      instance.message = request.data.get("message")
      instance.save()

      # serializer = self.get_serializer(data=instance)
      serializer = CommentSerializer(instance, data=request.data)
      serializer.is_valid(raise_exception=True)
      self.perform_update(serializer)
      return Response(serializer.data)


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

