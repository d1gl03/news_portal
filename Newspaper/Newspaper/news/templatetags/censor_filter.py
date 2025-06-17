from django import template
from django.utils.html import conditional_escape
from django.utils.safestring import mark_safe

register = template.Library()

BAD_WORDS = ['редиска', 'нежелательное', 'слово']  # Замените на ваш список


@register.filter(needs_autoescape=True)
def censor(value, autoescape=True):
    if autoescape:
        value = conditional_escape(value)

    for word in BAD_WORDS:
        replacement = word[0] + '*' * (len(word) - 1)
        value = value.replace(word, replacement)
        value = value.replace(word.capitalize(), replacement)

    return mark_safe(value)