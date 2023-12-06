from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.views import LoginView
from django.views.generic import CreateView, UpdateView
from .forms import ProfileUserForm, RegisterUserForm
from django.contrib.auth import logout
from django.urls import reverse_lazy
from .forms import LoginUserForm
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin


class LoginUser(LoginView):
    """Класс для авторизации пользователя
    Args:
        DataMixin (class): _description_
        LoginView (class): _description_
    """

    form_class = LoginUserForm
    template_name = "users/login.html"
    extra_context = {"title": "Авторизация"}

    # def get_success_url(self):
    #     """Получение страницы после авторизации пользователя"""
    #     return reverse_lazy("home")


def logout_user(request):
    """Получение перенаправления после авторизации пользователя"""

    logout(request)
    return HttpResponseRedirect(reverse("users:login"))


class RegisterUser(CreateView):
    """Класс для регистрации пользователя
    Args:
        DataMixin (class): _description_
        CreateView (class): _description_
    """

    form_class = RegisterUserForm
    template_name = "users/register.html"
    extra_context = {"title": "Регистрация"}
    success_url = reverse_lazy("users:login")


class ProfileUser(LoginRequiredMixin, UpdateView):
    """Класс для получения страницы с профилем пользователя"""

    model = get_user_model()
    form_class = ProfileUserForm
    template_name = "users/profile.html"
    extra_context = {"title": "Профиль пользователя"}

    def get_success_url(self):
        """Получение страницы с профилем пользователя"""
        return reverse_lazy("users:profile")

    def get_object(self, queryset=None):
        """Получение объектов для регистрации пользователя"""
        return self.request.user
