from django import forms
from dateutil.relativedelta import relativedelta
from django.core.files.storage import default_storage
from django.core.exceptions import ValidationError
from django.utils import timezone
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
        """Валидация email."""
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
        email = self.cleaned_data.get("email")
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

    def clean_first_name(self):
        """Валидация имени."""
        first_name = self.cleaned_data.get("first_name")
        if len(first_name) > 30:
            raise ValidationError("Имя не может быть длиннее 30 символов.")
        return first_name

    def clean_last_name(self):
        """Валидация фамилии."""
        last_name = self.cleaned_data.get("last_name")
        if len(last_name) > 30:
            raise ValidationError("Имя не может быть длиннее 30 символов.")
        return last_name

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
        if birth_date:
            max_age_date = timezone.now().date() - relativedelta(years=120)
            if birth_date < max_age_date:
                raise ValidationError("Возраст не может превышать 120 лет.")
            if birth_date > timezone.now().date():
                raise ValidationError("Дата рождения не может быть в будущем.")
        return birth_date

    def clean_email(self):
        """Валидация email."""
        email = self.cleaned_data.get("email").strip().lower()
        user_email = self.instance.email.strip().lower()
        if email != user_email and User.objects.filter(email=email).exists():
            raise ValidationError(f"{email} уже зарегистрирован.")
        return email

    def clean_profile_picture(self):
        """Валидация фото профиля."""
        new_photo = self.cleaned_data.get("profile_picture")
        if self.instance and new_photo:
            old_photo = self.instance.profile_picture
            if old_photo and old_photo.name != new_photo.name:
                if default_storage.exists(old_photo.name):
                    default_storage.delete(old_photo.name)
        if new_photo and new_photo.size > 5 * 1024 * 1024:
            raise ValidationError("Размер фото не должен превышать 5MB.")
        valid_image_extensions = [".jpg", ".jpeg", ".png"]
        if new_photo and not any(
            new_photo.name.lower().endswith(ext) for ext in valid_image_extensions
        ):
            raise ValidationError(
                "Файл должен быть изображением в формате .jpg, .jpeg, .png."
            )
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
        email = self.cleaned_data["email"]
        if not User.objects.filter(email=email).exists():
            raise forms.ValidationError(f"Пользователь {email} не найден.")
        return email
