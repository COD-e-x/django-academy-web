from django.shortcuts import render, redirect, reverse
from django.contrib.auth import authenticate, login, logout

from .forms import UserRegisterForm, UserLoginForm


def user_register(request):
    form = UserRegisterForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.set_password(form.cleaned_data["password"])
            new_user.save()
            return redirect("users:login")
    context = {
        "title": "Создать аккаунт",
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


def user_profile(request):
    context = {
        "title": f"Ваш профиль",
    }
    return render(
        request,
        "users/profile.html",
        context,
    )


def user_logout(request):
    logout(request)
    return redirect("dogs:index")
