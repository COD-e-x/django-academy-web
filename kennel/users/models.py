from django.db import models
from django.contrib.auth.models import AbstractUser

NULLABLE = {"null": True, "blank": True}
NULLABLE_FOR_STRING = {"null": False, "blank": True}


class User(AbstractUser):
    username = None
    first_name = models.CharField(
        max_length=30,
        **NULLABLE_FOR_STRING,
        verbose_name="Имя",
    )
    last_name = models.CharField(
        max_length=30,
        **NULLABLE_FOR_STRING,
        verbose_name="Фамилия",
    )
    email = models.EmailField(
        unique=True,
        verbose_name="Эл. почта",
    )
    phone = models.CharField(
        max_length=35,
        verbose_name="Номер телефона",
        **NULLABLE_FOR_STRING,
    )
    telegram = models.CharField(
        max_length=50,
        verbose_name="Телеграм",
        **NULLABLE_FOR_STRING,
    )
    birth_date = models.DateField(
        **NULLABLE,
        verbose_name="Дата рождения",
    )
    gender = models.CharField(
        max_length=1,
        choices=[
            ("М", "Мужской"),
            ("Ж", "Женский"),
        ],
        verbose_name="Пол",
        **NULLABLE,
    )
    profile_picture = models.ImageField(
        upload_to="profile_pictures/",
        **NULLABLE,
        verbose_name="Фото профиля",
    )
    address = models.CharField(
        max_length=255,
        **NULLABLE_FOR_STRING,
        verbose_name="Адрес",
    )
    # role = models.CharField(
    #     max_length=20,
    #     choices=[
    #         ("user", _("Пользователь")),
    #         ("moderator", _("Модератор")),
    #         ("admin", _("Администратор")),
    #     ],
    #     default="user",
    #     verbose_name=_("Роль"),
    # )
    status = models.CharField(
        max_length=10,
        choices=[
            ("active", "Активный"),
            ("inactive", "Неактивный"),
            ("banned", "Заблокирован"),
        ],
        default="active",
        verbose_name="Статус",
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name="Активен",
    )

    # email_verified = models.BooleanField(default=False, verbose_name=_("Email подтверждён"))
    # phone_verified = models.BooleanField(default=False, verbose_name=_("Телефон подтверждён"))
    # telegram_verified = models.BooleanField(default=False, verbose_name=_("Telegram подтверждён"))

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []


class Meta:
    verbose_name = "Пользователь"
    verbose_name_plural = "Пользователи"
    ordering = ["id"]


def __str__(self):
    return self.email


def get_full_name(self):
    return f"{self.first_name} {self.last_name}"


def get_short_name(self):
    return self.first_name


def activate(self):
    self.is_active = True
    self.save()


def deactivate(self):
    self.is_active = False
    self.save()
