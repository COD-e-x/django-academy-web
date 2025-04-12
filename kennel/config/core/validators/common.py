from typing import Optional, Any

from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import UploadedFile
from django.utils import timezone
from dateutil.relativedelta import relativedelta
from django.core.files.storage import default_storage


class DateValidator:
    """Валидация пароля."""

    @staticmethod
    def age_limit(
        birth_date: Optional[timezone.datetime.date],
        max_years: int = 120,
        label: str = "Объект",
    ) -> Optional[timezone.datetime.date]:
        if birth_date:
            today = timezone.now().date()
            max_age_date = today - relativedelta(years=max_years)
            if birth_date < max_age_date:
                raise ValidationError(
                    f"Возраст {label.lower()} не может превышать {max_years} лет."
                )
            if birth_date > today:
                raise ValidationError("Дата рождения не может быть в будущем.")
        return birth_date


class PhotoValidator:
    """Валидация фото."""

    @staticmethod
    def photo_size(new_photo: UploadedFile, max_size_mb: int = 5) -> UploadedFile:
        """Проверка размера фото."""
        if new_photo.size > max_size_mb * 1024 * 1024:
            raise ValidationError(f"Размер фото не должен превышать {max_size_mb}MB.")
        return new_photo

    @staticmethod
    def photo_extension(new_photo: UploadedFile) -> UploadedFile:
        """Проверка расширения фото."""
        valid_extensions = [".jpg", ".jpeg", ".png"]
        if not any(new_photo.name.lower().endswith(ext) for ext in valid_extensions):
            raise ValidationError(
                "Файл должен быть изображением в формате .jpg, .jpeg, .png."
            )
        return new_photo

    @staticmethod
    def delete_old_photo(
        instance: Any, field_name: str, new_file: Optional[UploadedFile]
    ) -> None:
        """
        Удаление старого файла, если он был заменён.
        :param instance: модуль, где есть поле с файлом
        :param field_name: строка — имя поля
        :param new_file: новый файл, пришедший на замену
        """
        if not instance or not new_file:
            return
        old_file = getattr(instance, field_name, None)
        if old_file and old_file.name != new_file.name:
            if default_storage.exists(old_file.name):
                default_storage.delete(old_file.name)
