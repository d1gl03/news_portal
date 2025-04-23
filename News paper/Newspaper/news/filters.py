from django_filters import FilterSet, CharFilter, DateFilter
from .models import Post
from django import forms

class PostFilter(FilterSet):
    title = CharFilter(
        label='Название',
        lookup_expr='icontains'
    )

    category = CharFilter(
        label='Категория',
        lookup_expr='exact'
    )

    author   = CharFilter(
        lookup_expr='icontains',
        label='Автор'
    )

    date_posted = DateFilter(
        lookup_expr='gt',
        label='Позже указанной даты',
        widget=forms.DateInput(attrs={'type': 'date'})
    )



    class Meta:
        model = Post
        fields = []