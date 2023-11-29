from django.db import models
from django.urls import reverse
from django.contrib.auth import get_user_model


class PublishedManager(models.Manager):
    """Описывает пользовательский менеджер записей для моделей.
    Args:
        models (class): _description_
    """

    def get_queryset(self):
        return super().get_queryset().filter(is_published=MyPhotos.Status.PUBLISHED)


class MyPhotos(models.Model):
    """Классы для модели MyPhotos.
    Args:
        models (class): _description_
    """

    class Status(models.IntegerChoices):
        """Формирует, автоматизирует процесс создания перечислений (0/1)
        определяет осмысленные имена, в которых они будут созданы.
        Args:
            models (int): _description_
        """

        DRAFT = 0, "Черновик"
        PUBLISHED = 1, "Опубликовано"

    title = models.CharField(max_length=255, verbose_name="Заголовок")
    slug = models.SlugField(
        max_length=255, unique=True, db_index=True, verbose_name="URL"
    )
    content = models.TextField(blank=True, verbose_name="Контент")
    photo = models.ImageField(
        upload_to="photos/%Y/%m/%d/",
        default=None,
        blank=True,
        null=True,
        verbose_name="Фото",
    )
    time_create = models.DateTimeField(auto_now_add=True, verbose_name="Время создания")
    time_update = models.DateTimeField(auto_now=True, verbose_name="Время изменения")
    is_published = models.BooleanField(
        choices=tuple(map(lambda x: (bool(x[0]), x[1]), Status.choices)),
        default=Status.DRAFT,
        verbose_name="Публикация",
    )
    cat = models.ForeignKey(
        "Category",
        on_delete=models.PROTECT,
        related_name="posts",
        verbose_name="Категории",
    )
    tags = models.ManyToManyField(
        "TagPost", blank=True, related_name="tags", verbose_name="Теги"
    )
    author = models.ForeignKey(
        get_user_model(),
        on_delete=models.SET_NULL,
        related_name="posts",
        null=True,
        default=None,
    )

    objects = models.Manager()
    published = PublishedManager()

    def __str__(self):
        """Возвращает строковое представление модели MyPhotos."""
        return self.title

    def get_absolute_url(self):
        """Возвращает путь до модели MyPhotos."""
        return reverse("post", kwargs={"post_slug": self.slug})

    class Meta:
        """Метаданные модели MyPhotos, устанавливает название модели."""

        verbose_name = "Мои фото"
        verbose_name_plural = "Мои фото"
        ordering = ["time_create", "title"]
        indexes = [models.Index(fields=["time_create"])]


class Category(models.Model):
    """Класс модели Category.
    Args:
        models (class): _description_
    """

    name = models.CharField(max_length=100, db_index=True, verbose_name="Категория")
    slug = models.SlugField(
        max_length=255, unique=True, db_index=True, verbose_name="URL"
    )

    def __str__(self):
        """Возвращает строковое представление модели Category."""
        return self.name

    def get_absolute_url(self):
        """Возвращает путь до модели Category."""
        return reverse("category", kwargs={"cat_slug": self.slug})

    class Meta:
        """Метаданные модели Category."""

        verbose_name = "Категории"
        verbose_name_plural = "Категории"
        ordering = ["id"]


class TagPost(models.Model):
    """Класс, описывающий модель TagPost. Реализация функционала
    тегирования записей.
    Args:
        models (class): _description_
    """

    tag = models.CharField(max_length=100, db_index=True, verbose_name="Тег")
    slug = models.SlugField(max_length=255, unique=True, db_index=True)

    def __str__(self):
        """Возвращает строковое представление модели TagPost."""
        return self.tag

    def get_absolute_url(self):
        """Формирует адрес для каждой конкретной записи тега"""
        return reverse("tag", kwargs={"tag_slug": self.slug})


class UploadFile(models.Model):
    file = models.FileField(upload_to="uploads_model")
