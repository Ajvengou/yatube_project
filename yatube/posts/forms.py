from django import forms

from .models import Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('text', 'group')
        labels = {
            'name': ('Writer'),
        }
        help_texts = {
            'name': ('Some useful help text.'),
        }
