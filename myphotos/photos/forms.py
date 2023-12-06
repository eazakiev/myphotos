from django import forms
from django.core.exceptions import ValidationError
from captcha.fields import CaptchaField
from .views import *
from .models import *


class AddPostForm(forms.ModelForm):
    """Класс формы для добавления поста
    Args:
        forms (class): _description_
    """

    def __init__(self, *args, **kwargs):
        """Конструктор формы для добавления поста"""
        super().__init__(*args, **kwargs)
        self.fields["cat"].empty_label = "Категория не выбрана"

    class Meta:
        """Метаданные для формы добавления поста"""

        model = MyPhotos
        fields = ["title", "slug", "content", "photo", "is_published", "cat", "tags"]
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-input"}),
            "content": forms.Textarea(attrs={"cols": 50, "rows": 5}),
        }

    def clean_title(self):
        """Кастомный валидатор для поля title, который проверяет наличие
        загруженного поста, не позволял вводить строку более 200 символов
        """
        title = self.cleaned_data["title"]
        if len(title) > 50:
            raise ValidationError("Длина превышает 50 символов")
        return title


class ContactForm(forms.Form):
    """Класс формы для отправки сообщения
    Args:
        forms (class): _description_
    """

    name = forms.CharField(label="Имя", max_length=255)
    email = forms.EmailField(label="Email")
    content = forms.CharField(
        label="Содержание", widget=forms.Textarea(attrs={"cols": 60, "rows": 10})
    )
    captcha = CaptchaField(label="Введите ответ")
