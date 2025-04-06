from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from .forms import UserRegisterForm, UserLoginForm


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
    """
    Вход пользователя в систему.
    Проверяет данные формы и аутентифицирует пользователя, если данные верны.
    """
    form = UserLoginForm(request.POST)
    if request.method == "POST":
        if form.is_valid():
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]
            user = authenticate(
                request,
                email=email,
                password=password,
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

@login_required(login_url='users:login')
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


def user_logout(request):
    """
    Выход пользователя.
    Завершающий сеанс и перенаправление на главную страницу.
    """
    logout(request)
    return redirect("dogs:index")
