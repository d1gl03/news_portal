from django.contrib.auth.models import User
from django.views.generic.edit import CreateView
from .models import BaseRegisterForm
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from news.models import Author
from django.contrib import messages
class BaseRegisterView(CreateView):
    model = User
    form_class = BaseRegisterForm
    success_url = '/'

@login_required
def upgrade_me(request):
    user = request.user

    # Получаем или создаем группу 'author'
    author_group, created = Group.objects.get_or_create(name='author')

    # Добавляем пользователя в группу (если ещё не в ней)
    if not user.groups.filter(name='author').exists():
        user.groups.add(author_group)
        messages.success(request, 'Поздравляем! Теперь вы автор!')

    # Создаем запись в модели Author, если её нет
    if not hasattr(user, 'author'):
        Author.objects.create(user=user)

    return redirect('/')