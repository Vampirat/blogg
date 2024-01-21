from django.forms import ModelForm
from django import forms

from .models import PostsModel


class NewPostForm(ModelForm):

    class Meta:
        model = PostsModel
        fields = ['title', 'text', 'picture',]
        labels = {
            'title': 'Тема',
            'text': 'Ваш пост',
            'picture': 'Картинка'
        }
        widgets = {
            'title': forms.TextInput(),
            'text': forms.Textarea(),
        }