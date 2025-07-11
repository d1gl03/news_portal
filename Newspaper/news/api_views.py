from rest_framework import viewsets, permissions
from .models import Post
from .serializers import PostSerializer

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def get_permissions(self):
        if self.request.method in permissions.SAFE_METHODS:
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]

class NewsViewSet(PostViewSet):
    def get_queryset(self):
        return Post.objects.filter(post_type='NW')

class ArticlesViewSet(PostViewSet):
    def get_queryset(self):
        return Post.objects.filter(post_type='AR')