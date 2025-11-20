# cases/templatetags/quiz_tags.py
from django import template

register = template.Library()

@register.filter(name="get_option")
def get_option(question, opt):
    return getattr(question, f"opt_{opt.lower()}")
