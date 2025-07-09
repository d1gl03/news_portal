from allauth.account.models import EmailAddress
from django.contrib.auth.models import User
from django.views.generic.edit import CreateView
from .models import BaseRegisterForm, EmailConfirmationCode
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from news.models import Author
from django.contrib import messages
class BaseRegisterView(CreateView):
    model = User
    form_class = BaseRegisterForm
    success_url = '/'


@login_required
def upgrade_me(request):
    user = request.user
    author_group, created = Group.objects.get_or_create(name='author')
    if not user.groups.filter(name='author').exists():
        user.groups.add(author_group)
        messages.success(request, 'Поздравляем! Теперь вы автор!')

    if not hasattr(user, 'author'):
        Author.objects.create(user=user)

    return redirect('/')



@login_required
def verify_code(request):
    if request.method == 'POST':
        code = request.POST.get('code')
        try:
            confirmation = EmailConfirmationCode.objects.get(
                user=request.user,
                code=code
            )
            email = EmailAddress.objects.get(user=request.user)
            email.verified = True
            email.save()
            confirmation.delete()
            return redirect('/')
        except EmailConfirmationCode.DoesNotExist:
            return render(request, 'verify_code.html', {'error': 'Неверный код'})

    return render(request, 'verify_code.html')