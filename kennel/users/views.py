import os
import random
import string

from django.http import HttpResponse
from django.shortcuts import render, reverse, redirect
from django.contrib.auth import (
    logout,
    update_session_auth_hash,
)
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import (
    LoginView,
    PasswordChangeView,
    LogoutView,
)
from django.views.generic import (
    CreateView,
    UpdateView,
)
from django.urls import reverse_lazy

from .models import User
from .forms import (
    UserRegisterForm,
    UserLoginForm,
    UserUpdateForm,
    UserPasswordChangeForm,
    UserEmailForm,
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
        "title": "Регистрация пользователя.",
    }

    def form_valid(self, form):
        send_register_email(form.clean_email())
        return super().form_valid(form)


class UserLoginView(LoginView):
    form_class = UserLoginForm
    template_name = "users/login.html"
    success_url = reverse_lazy("users:profile")
    redirect_authenticated_user = True  # Перенаправляет авторизованного пользователя. Что бы не регистрировался заново.
    extra_context = {
        "title": "Авторизация пользователя.",
    }


@login_required(login_url="users:login")
def user_profile(request):
    """
    Профиль пользователя.
    Отображает страницу профиля для авторизованных пользователей.
    """
    context = {
        "title": f"Ваш профиль",
    }
    return render(
        request,
        "users/profile.html",
        context,
    )


@login_required(login_url="users:login")
def user_update(request):
    """
    Обновление данных пользователя.
    Позволяет обновить профиль, включая фото.
    Удаляет старую фотографию при загрузке новой.
    """
    user_object = request.user
    if user_object.profile_picture:
        file_path = user_object.profile_picture.path
    else:
        file_path = None
    if request.method == "POST":
        form = UserUpdateForm(request.POST, request.FILES, instance=user_object)
        if form.is_valid():
            if "profile_picture" in request.FILES:
                if file_path:
                    if os.path.exists(file_path):
                        os.remove(file_path)
            user_object = form.save(commit=False)
            user_object.save()
            if "HX-Request" in request.headers:
                response = HttpResponse()
                response["HX-Redirect"] = "/users/profile/"
                return response
        else:
            return render(request, "users/user_includes/update.html", {"form": form})
    context = {
        "object": user_object,
        "form": UserUpdateForm(instance=user_object),
    }
    return render(
        request,
        "users/user_includes/update.html",
        context,
    )


@login_required(login_url="users:login")
def password_change(request):
    """
    Смена пароля пользователя.
    Обновляет пароль и сессию при успешной валидации формы.
    """
    user_object = request.user
    form = UserPasswordChangeForm(user_object or None, request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            user_object = form.save()
            update_session_auth_hash(request, user_object)
            if "HX-Request" in request.headers:
                response = HttpResponse()
                response["HX-Redirect"] = "/users/profile/"
                return response
    context = {
        "form": form,
    }
    return render(
        request,
        "users/user_includes/password-change.html",
        context,
    )


def user_logout(request):
    """
    Выход пользователя.
    Завершающий сеанс и перенаправление на главную страницу.
    """
    logout(request)
    return redirect("dogs:index")


def reset_password_success(request):
    return render(
        request,
        "users/reset-password-success.html",
    )


def reset_password(request):
    form = UserEmailForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            email = form.cleaned_data["email"]
            user = User.objects.get(email=email)
            new_password = "".join(
                random.sample((string.ascii_letters + string.digits), 12)
            )
            user.set_password(new_password)
            user.save()
            send_new_password(user.email, new_password)
            if "HX-Request" in request.headers:
                response = HttpResponse()
                response["HX-Redirect"] = "/users/reset-password-success"
                return response
    context = {
        "form": form,
    }
    return render(
        request,
        "users/reset-password.html",
        context,
    )
