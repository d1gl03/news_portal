from django_filters import FilterSet, CharFilter, DateFilter, ModelChoiceFilter
from .models import Post, Category
from django import forms

class PostFilter(FilterSet):
    title = CharFilter(
        label='Название',
        lookup_expr='icontains'
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

class CategoryFilter(FilterSet):
    category = ModelChoiceFilter(
        empty_label="Все категории",
        field_name='category',
        label="Выбор категории",
        queryset=Category.objects.all()
    )

    class Meta:
        model = Post  # Замените на вашу модель публикаций, если она иначе называется
        fields = []