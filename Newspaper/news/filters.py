from django_filters import FilterSet, CharFilter, DateFilter, ModelChoiceFilter
from .models import Post, Category
from django import forms
from django.utils.translation import gettext as _

class PostFilter(FilterSet):
    title = CharFilter(
        label=_('Название'),
        lookup_expr='icontains'
    )


    author   = CharFilter(
        lookup_expr='icontains',
        label=_('Автор')
    )

    date_posted = DateFilter(
        lookup_expr='gt',
        label=_('Позже указанной даты'),
        widget=forms.DateInput(attrs={'type': 'date'})
    )



    class Meta:
        model = Post
        fields = []

class CategoryFilter(FilterSet):
    category = ModelChoiceFilter(
        empty_label=_("Все категории"),
        field_name=_('category'),
        label=_("Выбор категории"),
        queryset=Category.objects.all()
    )

    class Meta:
        model = Post
        fields = []