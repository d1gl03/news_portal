from django.contrib.auth.views import LoginView
from django.urls import path, include
# Импортируем созданные нами представления
from .views import (PostListView, PostDetailView, PostDeleteView, PostUpdateView, ArticleCreateView, NewsCreateView)


urlpatterns = [

    path('', PostListView.as_view(), name='posts_list'),
    path('<int:pk>/', PostDetailView.as_view(), name='post_detail'),  # Добавили name и /
    path('news/create/', NewsCreateView.as_view(), name='news_create'),
    path('article/create/', ArticleCreateView.as_view(), name='article_create'),
    path('<int:pk>/edit/', PostUpdateView.as_view(), name='post_edit'),
    path('<int:pk>/delete/', PostDeleteView.as_view(), name='post_delete'),
    ]