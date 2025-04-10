import os
import random
import string

from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import (
    authenticate,
    login,
    logout,
    update_session_auth_hash,
)

from django.contrib.auth.decorators import login_required

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


def user_register(request):
    """
    Регистрация нового пользователя.
    Сохраняет пользователя, если форма валидна, и перенаправляет на страницу входа.
    """
    form = UserRegisterForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.set_password(form.cleaned_data["password"])
            new_user.save()
            send_register_email(new_user.email)
            return redirect("users:login")
    context = {
        "form": form,
    }
    return render(
        request,
        "users/register.html",
        context,
    )


def user_login(request):
    """
    Вход пользователя.
    Аутентифицирует пользователя и перенаправляет в профиль при успешном входе.
    """
    form = UserLoginForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            user = authenticate(
                request,
                email=form.cleaned_data["email"],
                password=form.cleaned_data["password"],
            )
            if user:
                login(request, user)
                return redirect("users:profile")
    context = {
        "form": form,
    }
    return render(
        request,
        "users/login.html",
        context,
    )


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
