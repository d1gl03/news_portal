from django.urls import path
from .views import (
    PostListView, PostDetailView,
    NewsCreateView, ArticleCreateView,
    PostUpdateView, PostDeleteView,
    CommentCreateView, subscribe, CommentModerationView
)
from django.views.decorators.cache import cache_page

urlpatterns = [
    path('', PostListView.as_view(), name='posts_list'),
    path('<int:pk>/', PostDetailView.as_view(), name='post_detail'),
    path('news/create/', cache_page(60 * 5)(NewsCreateView.as_view()), name='news_create'),
    path('article/create/', cache_page(60 * 5)(ArticleCreateView.as_view()), name='article_create'),
    path('<int:pk>/edit/', cache_page(60 * 5)(PostUpdateView.as_view()), name='post_edit'),
    path('<int:pk>/delete/', cache_page(60 * 5)(PostDeleteView.as_view()), name='post_delete'),
    path('subscribe/<int:category_id>/', subscribe, name='subscribe'),
    path('<int:pk>/comment/', CommentCreateView.as_view(), name='comment_create'),
    path('moderate/', CommentModerationView.as_view(), name='moderate'),
]