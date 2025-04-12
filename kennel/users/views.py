import random
import string

from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.views import (
    LoginView,
    PasswordChangeView,
    LogoutView,
)
from django.views.generic import (
    FormView,
    CreateView,
    DetailView,
    UpdateView,
)
from django.urls import reverse_lazy

from .models import User
from .forms import (
    UserRegisterForm,
    UserLoginForm,
    UserUpdateForm,
    UserPasswordChangeForm,
    UserEmailExistsForm,
)
from .services import (
    send_new_password,
    send_register_email,
)


class UserRegisterViews(CreateView):
    """
    Регистрация нового пользователя.
    Сохраняет пользователя, если форма валидна, и перенаправляет на страницу профиля.
    """

    model = User
    form_class = UserRegisterForm
    template_name = "users/register.html"
    success_url = reverse_lazy("users:login")
    extra_context = {
        "title": "Регистрация пользователя",
    }

    def form_valid(self, form):
        send_register_email(form.clean_email())
        return super().form_valid(form)


class UserLoginView(LoginView):
    """
    Вход пользователя.
    Аутентифицирует пользователя и перенаправляет в профиль при успешном входе.
    """

    form_class = UserLoginForm
    template_name = "users/login.html"
    redirect_authenticated_user = True  # Перенаправляет авторизованного пользователя. Что бы не регистрировался заново.
    extra_context = {
        "title": "Авторизация пользователя",
    }


class UserProfileView(DetailView):
    """
    Профиль пользователя.
    Отображает страницу профиля для авторизованных пользователей.
    """

    model = User
    template_name = "users/profile.html"
    extra_context = {
        "title": "Ваш профиль",
    }

    def get_object(self, queryset=None):
        return self.request.user


class UserUpdateView(UpdateView):
    """
    Обновление данных пользователя.
    Позволяет обновить профиль, включая фото.
    Удаляет старую фотографию при загрузке новой.
    """

    model = User
    form_class = UserUpdateForm
    template_name = "users/user_includes/update.html"
    success_url = reverse_lazy("users:profile")
    extra_context = {
        "title": "Изменение профиля",
    }

    def get_object(self, queryset=None):
        return self.request.user

    def form_valid(self, form):
        form.save()
        if "HX-Request" in self.request.headers:
            response = HttpResponse()
            response["HX-Redirect"] = self.get_success_url()
            return response
        return super().form_valid(form)


class UserPasswordChangeView(PasswordChangeView):
    """
    Смена пароля пользователя.
    Обновляет пароль и сессию при успешной валидации формы.
    """

    form_class = UserPasswordChangeForm
    template_name = "users/user_includes/password-change.html"
    success_url = reverse_lazy("users:login")
    extra_context = {
        "title": "Смена пароля",
    }

    def form_valid(self, form):
        form.save()
        if "HX-Request" in self.request.headers:
            response = HttpResponse()
            response["HX-Redirect"] = self.get_success_url()
            return response
        return super().form_valid(form)


class UserLogoutView(LogoutView):
    """
    Выход пользователя.
    Завершающий сеанс и перенаправление на главную страницу.
    """

    pass


def reset_password_success(request):
    return render(
        request,
        "users/reset-password-success.html",
    )


class UserResetPasswordView(FormView):
    form_class = UserEmailExistsForm
    template_name = "users/reset-password.html"
    success_url = reverse_lazy("users:reset-password-success")
    extra_context = {
        "title": "Восстановление пароля",
    }

    def form_valid(self, form):
        email = form.cleaned_data["email"]
        user = User.objects.get(email=email)
        new_password = "".join(
            random.sample((string.ascii_letters + string.digits), 12)
        )
        user.set_password(new_password)
        user.save()
        send_new_password(user.email, new_password)
        if "HX-Request" in self.request.headers:
            response = HttpResponse()
            response["HX-Redirect"] = self.get_success_url()
            return response
        return super().form_valid(form)
