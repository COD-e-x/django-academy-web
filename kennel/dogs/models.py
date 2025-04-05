from django.db import models

NULLABLE = {"null": True, "blank": True}
NULLABLE_FOR_STRING = {"null": False, "blank": True}


class Breed(models.Model):
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
    name = models.CharField(
        max_length=250,
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
    birth_date = models.DateTimeField(
        **NULLABLE,
        verbose_name="Дата рождения",
    )

    class Meta:
        verbose_name = "Собака"
        verbose_name_plural = "Собаки"

    def __str__(self):
        return f"{self.name} ({self.breed})"
