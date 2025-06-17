from django import forms
from .models import Post
from django.core.exceptions import ValidationError


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'author', 'category']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 5}),
        }

    def clean(self):
        cleaned_data = super().clean()
        content = cleaned_data.get('content')
        if len(content) < 30:
            raise ValidationError({
                'content': 'Контент должен содержать не менее 30 символов!'
            })
        title = cleaned_data.get('title')
        if not title:
            raise ValidationError({
                'title': 'Заголовок не может быть пустым!'
            })