from django import forms
from .models import Comment
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']


class CommentForm(forms.ModelForm):
    author_name = forms.CharField(label='Ваше имя',
                                  required=False,
                                  empty_value="Гость",
                                  widget=forms.TextInput(attrs={
        'placeholder': 'Потиханов Сергей'
    }))
    message = forms.CharField(label='Комментарий', widget=forms.Textarea(attrs={
        'rows': '3',
        'class': 'md-textarea form-control mb-2',
        'placeholder': 'Оставьте комментарий'
    }))



    class Meta:
        model = Comment
        fields = {'author_name', 'message'}
