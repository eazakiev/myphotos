from django.http import HttpResponseNotFound
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, FormView, UpdateView
from .forms import AddPostForm, ContactForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect, render

from .models import Category, MyPhotos, TagPost
from .utils import *


class PhotosHome(DataMixin, ListView):
    """Класс для получения главной страницы сайта
    Args:
        DataMixin (class): _description_
        ListView (class): _description_
    """

    template_name = "photos/index.html"
    context_object_name = "posts"
    cat_selected = 0

    def get_context_data(self, *, object_list=None, **kwargs):
        """Получение контекста для главной страницы сайта"""
        context = super().get_context_data(**kwargs)
        return self.get_mixin_context(context, title="Главная страница")

    def get_queryset(self):
        """Получение объектов для постов"""
        return MyPhotos.objects.filter(is_published=True).select_related("cat")


# @login_required(login_url=reverse_lazy("users:login"))
def about(request):
    """О сайте"""
    # contact_list = MyPhotos.published.all()
    # page_number = request.GET.get("page")
    return render(request, "photos/about.html", {"title": "О сайте", "menu": menu})


def pageNotFound(request, exception):
    """Получение сообщения страница не найдена"""
    return HttpResponseNotFound("<h1>Страница не найдена (Боевой сервер!)</h1>")


class AddPage(LoginRequiredMixin, DataMixin, CreateView):
    """Класс для добавления статьи
    Args:
        LoginRequiredMixin (class): _description_
        DataMixin (class): _description_
        CreateView (class): _description_
    """

    form_class = AddPostForm
    template_name = "photos/addpage.html"
    title_page = "Добавление статьи"
    success_url = reverse_lazy("home")
    # login_url = reverse_lazy("home")
    # raise_exception = True

    def get_context_data(self, *, object_list=None, **kwargs):
        """Получение контекста для добавления статьи"""
        context = super().get_context_data(**kwargs)
        return self.get_mixin_context(context, title="Добавление статьи")

    def form_valid(self, form):
        """Обработка формы добавления статьи"""
        w = form.save(commit=False)
        w.author = self.request.user
        return super().form_valid(form)


class UpdatePage(DataMixin, UpdateView):
    """Класс для редактирования статьи"""

    model = MyPhotos
    fields = ["title", "content", "photo", "is_published", "cat"]
    template_name = "photos/addpage.html"
    success_url = reverse_lazy("home")
    title_page = "Редактирование статьи"


class ContactFormView(DataMixin, FormView):
    """Класс для представления формы контактов
    Args:
        DataMixin (class): _description_
        FormView (class): Стандартный базовый класс для форм,
        не привязанных к моделям, не работает с БД
    """

    form_class = ContactForm
    template_name = "photos/contact.html"
    success_url = reverse_lazy("home")

    def get_context_data(self, *, object_list=None, **kwargs):
        """Получение контекста для шаблона, формы контактов"""
        context = super().get_context_data(**kwargs)
        return self.get_mixin_context(context, title="Обратная связь")

    def form_valid(self, form):
        """
        Обработка формы контактов, вызывается если пользователь
        корректно заполнил все поля контактной формы
        """
        print(form.cleaned_data)
        return redirect("home")


class ShowPost(DataMixin, DetailView):
    """Класс для представления статьи
    Args:
        DataMixin (class): _description_
        DetailView (class): _description_
    """

    template_name = "photos/post.html"
    slug_url_kwarg = "post_slug"
    context_object_name = "post"

    def get_context_data(self, *, object_list=None, **kwargs):
        """Получение контекста для представления статьи"""
        context = super().get_context_data(**kwargs)
        return self.get_mixin_context(context, title=context["post"].title)

    def get_object(self, queryset=None):
        return get_object_or_404(
            MyPhotos.published, slug=self.kwargs[self.slug_url_kwarg]
        )


class PhotosCategory(DataMixin, ListView):
    """Класс для получения списка категорий сайта
    Args:
        DataMixin (class): _description_
        ListView (class): _description_
    """

    template_name = "photos/index.html"
    context_object_name = "posts"
    allow_empty = False

    def get_queryset(self):
        """Получение объектов для списка категорий"""
        return MyPhotos.objects.filter(
            cat__slug=self.kwargs["cat_slug"], is_published=True
        ).select_related("cat")

    def get_context_data(self, **kwargs):
        """Получение контекста для списка категорий"""
        context = super().get_context_data(**kwargs)
        cat = Category.objects.get(slug=self.kwargs["cat_slug"])
        return self.get_mixin_context(
            context, title="Категория - " + cat.name, cat_selected=cat.pk
        )


class TagPostList(DataMixin, ListView):
    """Класс получение списка постов по тегу
    Args:
        DataMixin (class): _description_
        LoginView (class): _description_
    """

    template_name = "photos/index.html"
    context_object_name = "posts"
    allow_empty = False

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        tag = TagPost.objects.get(slug=self.kwargs["tag_slug"])
        return self.get_mixin_context(context, title="Тег: " + tag.tag)

    def get_queryset(self):
        return MyPhotos.published.filter(
            tags__slug=self.kwargs["tag_slug"]
        ).select_related("cat")


def confidential(request):
    """О политике конфиденциальности"""
    return render(
        request, "photos/confidential.html", {"title": "О сайте", "menu": menu}
    )


def terms(request):
    """О пользовательском соглашении"""
    return render(request, "photos/terms.html", {"title": "О сайте", "menu": menu})
