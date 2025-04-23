from django.core.mail import send_mail
from django.conf import settings

def send_notification_email(subject, message, recipient_list):
    email_from = settings.EMAIL_HOST_USER
    send_mail(subject, message, email_from, recipient_list)