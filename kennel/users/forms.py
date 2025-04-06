from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate

from .models import User
from .validators import PasswordValidator


class UserRegisterForm(forms.ModelForm):
    """Форма регистрации пользователя."""
    password = forms.CharField(
        label="Пароль",
        widget=forms.PasswordInput,
        min_length=8,
    )
    password2 = forms.CharField(
        label="Повторите пароль",
        widget=forms.PasswordInput,
        min_length=8,
    )

    class Meta:
        model = User
        fields = ("email",)

    def clean_password(self):
        """Валидация пароля."""
        password = self.cleaned_data.get("password")
        return PasswordValidator.validate_password(password)

    def clean_password2(self):
        """Валидация пароля."""
        cd = self.cleaned_data
        if cd.get("password") != cd.get("password2"):
            raise ValidationError("Пароли не совпадают!")
        return cd["password2"]

    def clean_email(self):
        """Валидация email"""
        email = self.cleaned_data.get("email").strip().lower()
        if User.objects.filter(email=email).exists():
            raise ValidationError("Этот email уже зарегистрирован!")
        return email


class UserLoginForm(forms.Form):
    """Форма авторизации пользователя."""
    email = forms.EmailField()
    password = forms.CharField(
        label="Пароль",
        widget=forms.PasswordInput,
        min_length=8,
    )

    def authenticate_user(self):
        """Проверка на существование пользователя в базе данных."""
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")
        if not email or not password:
            return None
        user = authenticate(email=email, password=password)  # Стандартный метод Django
        if not user:
            self.add_error(None, "Неверный email или пароль!")
            return None
        if not user.is_active:
            self.add_error(None, "Аккаунт деактивирован!")
            return None
        return user


class UserForm(forms.ModelForm):
    """Форма для пользователя."""

    class Meta:
        model = User
        fields = "__all__"
        exclude = ("is_active", "status")
