from datetime import timezone, timedelta

from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string

from .models import Post, Category

@shared_task
def notify_subscribers(post_id):
    post = Post.objects.get(id=post_id)
    categories = post.category.all()
    for category in categories:
        subscribers = category.subscribers.all()
        for user in subscribers:
            send_mail(
                subject=f'Новая новость в категории {category.name}!',
                message=f'Заголовок: {post.title}\n\n{post.content[:50]}...',
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[user.email],
            )

@shared_task
def weekly_newsletter():
    last_week = timezone.now() - timedelta(days=7)
    categories = Category.objects.all()
    for category in categories:
        posts = Post.objects.filter(category=category, created_at__gte=last_week)
        if posts.exists():
            subscribers = category.subscribers.all()
            for user in subscribers:
                html_content = render_to_string('weekly_newsletter.html', {
                    'category': category,
                    'posts': posts,
                })
                send_mail(
                    subject=f'Еженедельная подборка новостей в категории {category.name}',
                    message='',
                    html_message=html_content,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[user.email],
                )