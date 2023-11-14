from django import template
from photos.models import *
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


# @register.simple_tag(name="getcats")
# def get_categories(filter=None):
#     """Получение списка категорий."""
#     if not filter:
#         return Category.objects.all()
#     else:
#         return Category.objects.filter(pk=filter)


# @register.inclusion_tag("photos/list_categories.html")
# def show_categories(sort=None, cat_selected=0):
#     """Показать список категорий."""
#     if not sort:
#         cats = Category.objects.all()
#     else:
#         cats = Category.objects.order_by(sort)

#     return {"cats": cats, "cat_selected": cat_selected}
