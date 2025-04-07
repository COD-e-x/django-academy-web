import os

from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from .forms import UserRegisterForm, UserLoginForm, UserUpdateForm


def user_register(request):
    """
    Регистрация нового пользователя.
    Сохраняет пользователя, если форма валидна, и перенаправляет на страницу входа.
    """
    form = UserRegisterForm(request.POST)
    if request.method == "POST":
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.set_password(form.cleaned_data["password"])
            new_user.save()
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
    form = UserLoginForm(request.POST)
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


def user_logout(request):
    """
    Выход пользователя.
    Завершающий сеанс и перенаправление на главную страницу.
    """
    logout(request)
    return redirect("dogs:index")
