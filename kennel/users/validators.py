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
            raise ValidationError(
                "Допустимы только английские буквы, цифры или @#$%^&+=!*()-!"
            )
        return password


class PhoneNumberValidator:
    """Валидация номера телефона для стран СНГ."""

    @staticmethod
    def validate_phone(phone):
        """Проверяет номер телефона на соответствие формату стран СНГ."""
        if not phone:
            return ""
        phone = re.sub(r"[^0-9+]", "", phone)
        # Допустимы коды стран СНГ
        phone_pattern = r"^\+?(7|8|3[8-9]|[9][8-9])(\d{10})$"
        if not re.fullmatch(phone_pattern, phone):
            raise ValidationError(
                "Неверный формат номера телефона для стран СНГ. Пример: +79991112233 / 89991112233"
            )
        return phone


class TelegramUsernameValidator:
    """Валидация имени пользователя для Telegram."""

    @staticmethod
    def validate_telegram(telegram):
        """Проверяет имя пользователя на соответствие формату Telegram."""
        if not telegram:
            return ""
        if telegram.startswith("@"):
            telegram = telegram[1:]
        username_pattern = r"^[A-Za-z0-9_-]{5,32}$"
        if not re.fullmatch(username_pattern, telegram):
            raise ValidationError(
                "Имя пользователя должно содержать от 5 до 32 символов и может включать только латинские буквы, цифры, дефисы и подчеркивания."
            )
        if telegram[0] in "_-" or telegram[-1] in "_-":
            raise ValidationError(
                "Имя пользователя не может начинаться или заканчиваться на символ подчеркивания или дефиса."
            )
        return telegram
