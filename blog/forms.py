from django import forms

from django_summernote.fields import SummernoteTextFormField

from .models import Post, Comment


class WysiwygForm(forms.ModelForm):
    content = SummernoteTextFormField()

    class Meta:
        model = Post
        fields = ['title', 'content']


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['author', 'email', 'content']
        labels = {
            'author': 'Name',
            'email': 'Email',
            'content': 'Comment'
        }



