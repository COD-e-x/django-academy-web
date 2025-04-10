from django import forms
from django.core.exceptions import ValidationError
from dateutil.relativedelta import relativedelta
from django.utils import timezone

from .models import Dog


class DogForm(forms.ModelForm):
    """Форма дял собак."""

    class Meta:
        model = Dog
        fields = "__all__"
        widgets = {
            "birth_date": forms.DateInput(
                attrs={"placeholder": "дд.мм.гггг", "class": "form-control"}
            ),
        }
        exclude = ("owner",)

    def clean_name(self):
        """Валидация имени"""
        name = self.cleaned_data.get("name")
        if len(name) < 2:
            raise ValidationError("Имя должно содержать минимум 2 символа.")
        if len(name) > 30:
            raise ValidationError("Имя не может быть длиннее 30 символов.")
        return name

    def clean_birth_date(self):
        """Валидация даты рождения"""
        birth_date = self.cleaned_data.get("birth_date")
        if birth_date:
            max_age_date = timezone.now().date() - relativedelta(years=35)
            if birth_date < max_age_date:
                raise ValidationError("Возраст собаки не может превышать 35 лет.")
            if birth_date > timezone.now().date():
                raise ValidationError("Дата рождения не может быть в будущем.")
        return birth_date

    def clean_photo(self):
        """Валидация фото"""
        photo = self.cleaned_data.get("photo")
        if photo and photo.size > 5 * 1024 * 1024:
            raise ValidationError("Размер фото не должен превышать 5MB.")
        valid_image_extensions = [".jpg", ".jpeg", ".png"]
        if photo and not any(
            photo.name.lower().endswith(ext) for ext in valid_image_extensions
        ):
            raise ValidationError(
                "Файл должен быть изображением в формате .jpg, .jpeg, .png."
            )
        return photo
