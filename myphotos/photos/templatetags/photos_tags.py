from django import template
from photos.models import *
from photos.utils import menu
from django.db.models import Count


register = template.Library()


@register.inclusion_tag("photos/list_categories.html")
def show_categories(cat_selected=0):
    """Показать список категорий."""
    cats = Category.objects.annotate(total=Count("posts")).filter(total__gt=0)
    return {"cats": cats, "cat_selected": cat_selected}


@register.inclusion_tag("photos/list_tags.html")
def show_all_tags():
    """Показать список тегов."""
    return {"tags": TagPost.objects.annotate(total=Count("tags")).filter(total__gt=0)}


@register.simple_tag(name="getcats")
def get_categories(filter=None):
    """Получение списка категорий."""
    if not filter:
        return Category.objects.all()
    else:
        return Category.objects.filter(pk=filter)


@register.simple_tag
def get_menu():
    """Получение меню."""
    return menu
