from allauth.account.forms import SignupForm
from .models import EmailConfirmationCode
from django.core.mail import send_mail
from django.conf import settings

from django.urls import reverse
from django.shortcuts import redirect


class CustomSignupForm(SignupForm):
    def save(self, request):
        user = super().save(request)
        user.is_active = False
        user.save()
        confirmation = EmailConfirmationCode.objects.create(user=user, code="123456")
        self.send_confirmation_email(user, confirmation.code)
        return user

    def send_confirmation_email(self, user, code):
        subject = 'Код подтверждения'
        message = f'Ваш код: {code}'
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user.email])