
from django.urls import path
# Импортируем созданные нами представления
from .views import (PostListView, PostDetailView, PostDeleteView, PostUpdateView, ArticleCreateView, NewsCreateView)
from . import views

from django.views.decorators.cache import cache_page
urlpatterns = [

    path('', PostListView.as_view(), name='posts_list'),
    path('<int:pk>/',PostDetailView.as_view(), name='post_detail'),  # Добавили name и /
    path('news/create/', cache_page(60 * 5)(NewsCreateView.as_view()), name='news_create'),
    path('article/create/', cache_page(60 * 5)(ArticleCreateView.as_view()), name='article_create'),
    path('<int:pk>/edit/', cache_page(60 * 5)(PostUpdateView.as_view()), name='post_edit'),
    path('<int:pk>/delete/', cache_page(60 * 5)(PostDeleteView.as_view()), name='post_delete'),
    path('subscribe/<int:category_id>/', views.subscribe, name='subscribe'),
    ]