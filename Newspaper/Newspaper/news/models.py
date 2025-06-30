from django.contrib.auth.models import User
from django.db import models
from datetime import datetime
from django.db.models import Sum
from django.urls import reverse
from django.db.models.signals import post_save
from django.dispatch import receiver


class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_rating = models.IntegerField(default=0)
    def uptade_rating(self):
        # 1. Сумма рейтингов всех статей автора × 3
        post_rating = Post.objects.filter(author=self).aggregate(
            total=Sum('rating')
        )['total'] or 0
        post_rating *= 3

        # 2. Сумма рейтингов всех комментариев автора
        comment_rating = Comment.objects.filter(user=self.user).aggregate(
            total=Sum('rating')
        )['total'] or 0

        # 3. Сумма рейтингов всех комментариев к статьям автора
        post_comments_rating = Comment.objects.filter(
            post__author=self
        ).aggregate(
            total=Sum('rating')
        )['total'] or 0

    def __str__(self):
        return self.user.username

class Category(models.Model):
    category_name = models.CharField(max_length=100, unique=True)
    subscribers = models.ManyToManyField(User, related_name='subscribers', blank=True)


    def __str__(self):
        return self.category_name

class Post(models.Model):
    ARTICLE = 'AR'
    NEWS = 'NW'
    POST_TYPES = [
        (ARTICLE, 'Статья'),
        (NEWS, 'Новость'),
    ]
    post_type = models.CharField(max_length=2, choices=POST_TYPES, default=ARTICLE)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    date_posted = models.DateTimeField(default=datetime.now)
    category = models.ManyToManyField(Category, through='PostCategory', related_name='posts')
    title = models.CharField(
        max_length=200)
    content = models.TextField()
    rating = models.IntegerField(default=0)
    image = models.ImageField(upload_to='posts/images/', blank=True, null=True)
    video = models.FileField(upload_to='posts/videos/', blank=True, null=True)
    file = models.FileField(upload_to='posts/files/', blank=True, null=True)
    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def preview(self):
        return self.content[:124] + '...'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post_detail', args=[str(self.id)])

class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment_text = models.TextField()
    comment_date = models.DateTimeField(default=datetime.now)
    rating = models.IntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

@receiver(post_save, sender=Post)
def post_created(sender, instance, created, **kwargs):
    if created:
        from .tasks import notify_subscribers
        notify_subscribers.delay(instance.id)