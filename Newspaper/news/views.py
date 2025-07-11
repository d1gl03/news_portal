from django.contrib.auth.decorators import login_required
from django.core.mail import EmailMultiAlternatives
from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post, Category, PostCategory, Comment, Author
from  datetime import  datetime
from .filters import PostFilter, CategoryFilter
from django.urls import reverse_lazy, reverse
from .forms import PostForm, CommentForm
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.views import LoginView
from .utils import send_notification_email
from .mixins import DailyPostLimitMixin
from django.core.cache import cache
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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['accepted_comments'] = self.object.comments.filter(status='accepted')
        return context

    # def get_object(self, *args, **kwargs):
    #     obj = cache.get(f'post-{self.kwargs["pk"]}', None)
    #     if obj is None:
    #         obj = super().get_object()
    #         cache.set(f'post-{self.kwargs["pk"]}', obj)
    #     return obj



class NewsCreateView(LoginRequiredMixin, DailyPostLimitMixin, CreateView):
    permission_required = ('news.add.Post')
    model = Post
    form_class = PostForm
    template_name = 'post_edit.html'
    success_url = reverse_lazy('posts_list')
    post_type = "NW"
    def form_valid(self, form):
        post = form.save(commit=False)
        post.post_type = 'NW'
        return super().form_valid(form)


class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = CommentForm
    template_name = 'comment_edit.html'
    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.post = get_object_or_404(Post, pk=self.kwargs['pk'])
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('post_detail', kwargs={'pk': self.object.post.pk})

# class CommentModerationList(LoginRequiredMixin, ListView):
#     model = Comment
#     template_name = 'moderation_list.html'
#     context_object_name = 'comments'
#     def get_queryset(self):
#         # Показываем только комментарии к постам текущего автора
#         return Comment.objects.filter(
#             post__author__user=self.request.user,
#             status=Comment.STATUS_PENDING
#         )


class CommentModerationView(LoginRequiredMixin, ListView):
    model = Comment
    template_name = 'moderate.html'
    context_object_name = 'comments'

    def get_queryset(self):
        author = get_object_or_404(Author, user=self.request.user)
        return Comment.objects.filter(
            post__author=author
        ).select_related('post', 'user')

    def post(self, request, *args, **kwargs):
        comment_id = request.POST.get('comment_id')
        action = request.POST.get('action')
        comment = get_object_or_404(Comment, id=comment_id)

        if action == 'accept':
            comment.status = Comment.STATUS_ACCEPTED
            comment.save()
        elif action == 'reject':
            comment.status = Comment.STATUS_REJECTED
            comment.save()
        elif action == 'delete':
            comment.delete()

        return redirect('moderate')



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
    post_type = "AR"
    def form_valid(self, form):
        post = form.save(commit=False)
        post.post_type = 'AR'
        post.save()
        return super().form_valid(form)

class LoginViev(LoginView):
    template_name = 'login.html'


@receiver(m2m_changed, sender=Post.category.through)
def send_notifications(sender, instance, action, **kwargs):
    if action == "post_add":
        categories = instance.category.all()
        for category in categories:
            subscribers = category.subscribers.all()
            for subscriber in subscribers:
                # Формируем HTML-письмо
                html_content = render_to_string(
                    'post_notification.html',
                    {
                        'post': instance,
                        'username': subscriber.username,
                    }
                )

                msg = EmailMultiAlternatives(
                    subject=instance.title,  # Заголовок статьи как тема письма
                    body='',  # Текстовое содержимое пустое, т.к. используем HTML
                    from_email='newsportal121@yandex.ru',
                    to=[subscriber.email],
                )
                msg.attach_alternative(html_content, "text/html")
                msg.send()


