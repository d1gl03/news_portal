from django.db.models.signals import post_save
from django.dispatch import receiver
from allauth.account.models import EmailAddress
from .models import EmailConfirmationCode

@receiver(post_save, sender=EmailConfirmationCode)
def set_email_unconfirmed(sender, instance, created, **kwargs):
    if created:
        email = EmailAddress.objects.get(user=instance.user)
        email.verified = False
        email.save()