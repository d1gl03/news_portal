from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from .models import Comment

@receiver(post_save, sender=Comment)
def handle_comment_notifications(sender, instance, created, **kwargs):
    if created:
        send_new_comment_notification(instance)
    else:
        old_status = Comment.objects.get(pk=instance.pk).status if not created else None
        if old_status != instance.status:
            send_comment_status_notification(instance)


def send_new_comment_notification(comment):
    subject = f'Новый комментарий к вашему посту "{comment.post.title}"'
    html_message = render_to_string('emails/new_comment.html', {
        'post': comment.post,
        'comment': comment,
        'site_url': settings.SITE_URL
    })

    send_mail(
        subject=subject,
        message='',
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[comment.post.author.user.email],
        html_message=html_message
    )


def send_comment_status_notification(comment):
    if comment.status == 'accepted':
        subject = f'Ваш комментарий принят (пост "{comment.post.title}")'
        template = 'emails/comment_accepted.html'
    elif comment.status == 'rejected':
        subject = f'Ваш комментарий отклонен (пост "{comment.post.title}")'
        template = 'emails/comment_rejected.html'
    else:
        return

    html_message = render_to_string(template, {
        'post': comment.post,
        'comment': comment,
        'site_url': settings.SITE_URL
    })

    send_mail(
        subject=subject,
        message='',
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[comment.user.email],
        html_message=html_message
    )