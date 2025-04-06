import re
from django.core.exceptions import ValidationError


class PasswordValidator:
    """Валидация пароля."""

    @staticmethod
    def validate_password(password):
        """Проверяет пароль на соответствие требованиям."""
        if len(password) < 8:
            raise ValidationError("Пароль должен быть не менее 8 символов!")
        if not re.fullmatch(r"[A-Za-z0-9@#$%^&+=!*()-]+", password):
            raise ValidationError("Допустимы только английские буквы, цифры или @#$%^&+=!*()-!")
        return password