from django import forms

from .models import Post, Comment

from django.forms import ModelForm
# from .models import Comments



class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = [
        "title",
        "content",
        "image",
        "draft",
        "publish",
        ]

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['author', 'text']