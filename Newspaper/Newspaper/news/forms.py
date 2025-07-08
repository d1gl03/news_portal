from django import forms
from .models import Post, Comment
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'author', 'category', 'image', 'video', 'file']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 5}),
        }

    def clean(self):
        cleaned_data = super().clean()
        content = cleaned_data.get('content')
        if len(content) < 30:
            raise ValidationError({
                'content': _('Контент должен содержать не менее 30 символов!')
            })
        title = cleaned_data.get('title')
        if not title:
            raise ValidationError({
                'title': _('Заголовок не может быть пустым!')
            })


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['comment_text']
        widgets = {
            'comment_text': forms.Textarea(attrs={
                'rows': 4,
                'class': 'form-control',
                'placeholder': 'Оставьте ваш комментарий...'
            }),
        }

    def clean_comment_text(self):
        comment_text = self.cleaned_data.get('comment_text')
        if len(comment_text.strip()) < 10:
            raise forms.ValidationError("Комментарий должен содержать минимум 10 символов")
        return comment_text