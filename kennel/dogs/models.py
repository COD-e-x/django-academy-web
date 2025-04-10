from django.db import models
from django.conf import settings

NULLABLE = {"null": True, "blank": True}
NULLABLE_FOR_STRING = {"null": False, "blank": True}


class Breed(models.Model):
    """Модель для породы."""

    name = models.CharField(
        max_length=100,
        verbose_name="Порода",
    )
    description = models.CharField(
        max_length=1000,
        verbose_name="Описание",
        **NULLABLE_FOR_STRING,
    )
    photo = models.ImageField(
        upload_to="breed/",
        **NULLABLE,
        verbose_name="Фото",
    )

    class Meta:
        verbose_name = "Порода собаки"
        verbose_name_plural = "Породы собак"

    def __str__(self):
        return f"{self.name}"


class Dog(models.Model):
    """Модель для собаки."""

    name = models.CharField(
        max_length=30,
        verbose_name="Имя",
    )
    breed = models.ForeignKey(
        Breed,
        on_delete=models.CASCADE,
        verbose_name="Порода",
    )
    photo = models.ImageField(
        upload_to="dogs/",
        **NULLABLE,
        verbose_name="Фото",
    )
    birth_date = models.DateField(
        **NULLABLE,
        verbose_name="Дата рождения",
    )
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        **NULLABLE,
        verbose_name="Хозяин",
    )

    class Meta:
        verbose_name = "Собака"
        verbose_name_plural = "Собаки"

    def __str__(self):
        return f"{self.name} ({self.breed})"
