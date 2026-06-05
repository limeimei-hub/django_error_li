from .models import Post
from django import forms

class PostForm(forms.ModelForm):
    class Meta:
        model = Posts
        fields = ['content']
