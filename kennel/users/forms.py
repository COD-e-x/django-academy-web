from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import (
    PasswordChangeForm,
    UserCreationForm,
)

from .models import User
from .validators import (
    PasswordValidator,
    PhoneNumberValidator,
    TelegramUsernameValidator,
)
from config.core.validators.common import (
    DateValidator,
    PhotoValidator,
)


class UserForm(forms.ModelForm):
    """Форма для пользователя."""

    class Meta:
        model = User
        exclude = ("is_active", "status")


class UserRegisterForm(UserCreationForm):
    """Форма регистрации пользователя."""

    class Meta:
        model = User
        fields = ("email",)

    def clean_password2(self):
        """Проверка на совпадение паролей."""
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        PasswordValidator.validate_password(password1)
        if password1 and password2 and password1 != password2:
            raise ValidationError("Пароли не совпадают.")
        return password2

    def clean_email(self):
        """Валидация email для регистрации."""
        email = self.cleaned_data.get("email").strip().lower()
        if User.objects.filter(email=email).exists():
            raise ValidationError(f'Увы, адрес "{email}" уже занят. Попробуйте другой.')
        return email


class UserLoginForm(forms.Form):
    """Форма авторизации пользователя с email"""

    email = forms.EmailField(
        label="Эл. почта",
        # validators=[validate_custom_email],
    )
    password = forms.CharField(
        label="Пароль",
        widget=forms.PasswordInput,
        min_length=8,
    )

    def __init__(self, *args, **kwargs):
        kwargs.pop("request", None)
        super().__init__(*args, **kwargs)

    def clean_password(self):
        """Валидация пароля."""
        password = self.cleaned_data.get("password")
        return PasswordValidator.validate_password(password)

    def clean(self):
        """
        Проверка существует ли пользователь в базе.
        Проверка блокировки доступа к аккаунту.
        """
        email = self.cleaned_data.get("email").strip().lower()
        password = self.cleaned_data.get("password")
        if email and password:
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                self.add_error("email", ValidationError("Неверный email."))
                return self.cleaned_data
            if not user.check_password(password):
                self.add_error("password", ValidationError("Неверный пароль."))
                return self.cleaned_data
            if not user.is_active:
                raise ValidationError(
                    "Доступ заблокирован, обратитесь к администрации сайта."
                )
            self.user_cache = user
        return self.cleaned_data

    def get_user(self):
        """Возвращает аутентифицированного пользователя из кеша формы.
        Returns:
            User: Объект пользователя, сохранённый после успешной валидации в clean().
        """
        return self.user_cache


class UserUpdateForm(forms.ModelForm):
    """Форма для обновления данных пользователя."""

    class Meta:
        model = User
        fields = (
            "first_name",
            "last_name",
            "email",
            "phone",
            "telegram",
            "birth_date",
            "gender",
            "address",
            "profile_picture",
        )
        widgets = {
            "birth_date": forms.DateInput(
                attrs={"placeholder": "дд.мм.гггг", "class": "form-control"}
            ),
        }

    def clean_phone(self):
        """Валидация номера телефона."""
        phone = self.cleaned_data.get("phone")
        return PhoneNumberValidator.validate_phone(phone)

    def clean_telegram(self):
        """Валидация номера телеграмм."""
        telegram = self.cleaned_data.get("telegram")
        return TelegramUsernameValidator.validate_telegram(telegram)

    def clean_birth_date(self):
        """Валидация даты рождения"""
        birth_date = self.cleaned_data.get("birth_date")
        return DateValidator.age_limit(birth_date, 120, "человека")

    def clean_email(self):
        """Валидация email для обновления."""
        email = self.cleaned_data.get("email").strip().lower()
        user_email = self.instance.email.strip().lower()
        if email != user_email and User.objects.filter(email=email).exists():
            raise ValidationError(f"{email} уже зарегистрирован.")
        return email

    def clean_profile_picture(self):
        """Валидация фото профиля."""
        new_photo = self.cleaned_data.get("profile_picture")
        if not new_photo:
            return
        PhotoValidator.photo_size(new_photo)
        PhotoValidator.photo_extension(new_photo)
        PhotoValidator.delete_old_photo(self.instance, "profile_picture", new_photo)
        return new_photo


class UserPasswordChangeForm(PasswordChangeForm):
    """Форма для смены пароля."""

    def clean_new_password2(self):
        password1 = self.cleaned_data.get("new_password1")
        password2 = self.cleaned_data.get("new_password2")
        PasswordValidator.validate_password(password1)
        if password1 and password2 and password1 != password2:
            raise ValidationError("Пароли не совпадают.")
        return password2

    def save(self, commit=True):
        """
        Сохраняет новый пароль пользователя в БД.
        Обновляет сессию.
        """
        password = self.cleaned_data["new_password1"]
        self.user.set_password(password)
        if commit:
            self.user.save()
        return self.user


class UserEmailExistsForm(forms.Form):
    """Форма для проверки наличия в базе почты."""

    email = forms.EmailField(
        label="Эл. почта",
        widget=forms.EmailInput(
            attrs={"placeholder": "Введите вашу почту", "class": "form-control"}
        ),
    )

    def clean_email(self):
        """Валидация email, проверка на наличие в базе."""
        email = self.cleaned_data.get("email").strip().lower()
        if not User.objects.filter(email=email).exists():
            raise forms.ValidationError(f"Пользователь {email} не найден.")
        return email
