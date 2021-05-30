from django import forms
from .models import Comment
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']


class CommentForm(forms.ModelForm):
    message = forms.CharField(label='Комментарий', widget=forms.Textarea(attrs={
        'rows': '3',
        'class': 'md-textarea form-control mb-2',
        'placeholder': 'Оставьте комментарий'
    }))



    class Meta:
        model = Comment
        fields = {'message'}
