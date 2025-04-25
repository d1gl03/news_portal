from django.core.mail import send_mail
from django.conf import settings

def send_notification_email(subject, message, recipient_list):
    from_email = 'newsportal121@yandex.ru'
    send_mail(subject, message, from_email, recipient_list)