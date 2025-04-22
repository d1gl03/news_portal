from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post, Category
from  datetime import  datetime
from .filters import PostFilter
from django.urls import reverse_lazy
from .forms import PostForm
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.views import LoginView

class PostListView(ListView):
    model = Post
    context_object_name = 'posts'
    ordering = ['-date_posted']
    template_name = 'search.html'
    paginate_by = 10

    def __init__(self):
        super().__init__()
        self.filterset = None
        self.category = Category.objects.all()

    def get_context_data(self, **kwargs):
        # Получаем базовый контекст
        context = super().get_context_data(**kwargs)
        # Добавляем текущее время
        context['time_now'] = datetime.utcnow()
        # Добавляем количество всех новостей
        context['news_count'] = self.get_queryset().count()
        context['filterset'] = self.filterset
        context['categories'] = self.category
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset=queryset)
        return self.filterset.qs

class PostDetailView(DetailView):
    model = Post
    context_object_name = 'post'
    template_name = 'news_detail.html'
    success_url = reverse_lazy('posts_list')

class NewsCreateView(PermissionRequiredMixin, CreateView):
    permission_required = ('news.add.Post')
    model = Post
    form_class = PostForm
    template_name = 'post_edit.html'
    success_url = reverse_lazy('posts_list')
    def form_valid(self, form):
        post = form.save(commit=False)
        post.post_type = 'NW'
        return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    permission_required = ('news.change.Post')
    model = Post
    form_class = PostForm
    template_name = 'post_edit.html'
    success_url = reverse_lazy('posts_list')


class PostDeleteView(PermissionRequiredMixin, DeleteView):
    permission_required = ('news.delete.Post')
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('posts_list')

class ArticleCreateView(PermissionRequiredMixin, CreateView):
    permission_required = ('news.add.Post')
    model = Post
    form_class = PostForm
    template_name = 'post_edit.html'
    success_url = reverse_lazy('posts_list')

    def form_valid(self, form):
        post = form.save(commit=False)
        post.post_type = 'AR'
        post.save()
        return super().form_valid(form)

class LoginViev(LoginView):
    template_name = 'login.html'


