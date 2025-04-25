from django.contrib.auth.decorators import login_required
from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post, Category, PostCategory
from  datetime import  datetime
from .filters import PostFilter, CategoryFilter
from django.urls import reverse_lazy
from .forms import PostForm
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.views import LoginView
from .utils import send_notification_email

@login_required
def subscribe(request, category_id):
    category = Category.objects.get(id=category_id)
    if request.method == 'POST':
        if request.user not in category.subscribers.all():
            category.subscribers.add(request.user)
            return redirect('posts_list')
    return render(request, 'subscribe.html', {'category': category})

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
        self.filterset_category = CategoryFilter(self.category)

    def get_context_data(self, **kwargs):
        # Получаем базовый контекст
        context = super().get_context_data(**kwargs)
        # Добавляем текущее время
        context['time_now'] = datetime.utcnow()
        # Добавляем количество всех новостей
        context['news_count'] = self.get_queryset().count()
        context['filterset'] = self.filterset
        context['categories'] = self.category
        context['filterset_category'] = self.filterset_category
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

@receiver(m2m_changed, sender=PostCategory)
def send_notification(sender, instance, **kwargs):
    """
    Отправляет уведомление на электронную почту подписчиков категории при создании или обновлении публикации.
    """
    if kwargs["action"] == "post_add":
        categories = instance.category.all()
        subject = f'Новое публикация'
        message = f'Добрый день,\n\nесть новая публикация:\n\n{instance.title}\n{instance.content[:500]}...'
        recipient_list = []
        for category in categories:
            recipient_list.extend([subscriber.email for subscriber in category.subscribers.all()])
        send_notification_email(subject, message, recipient_list)
