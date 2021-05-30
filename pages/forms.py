from django import forms
from .models import Comment

class CommentForm(forms.ModelForm):
    author_name = forms.CharField(label='Ваше имя',
                                  required=False,
                                  empty_value="Гость",
                                  widget=forms.TextInput(attrs={
        'placeholder': 'Ваше имя'
    }))
    message = forms.CharField(label='Комментарий', widget=forms.Textarea(attrs={
        'rows': '3',
        'class': 'md-textarea form-control mb-2',
        'placeholder': 'Оставьте комментарий'
    }))



    class Meta:
        model = Comment
        fields = {'author_name', 'message'}