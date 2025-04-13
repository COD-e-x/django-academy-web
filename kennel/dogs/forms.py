from django import forms
from django.core.exceptions import ValidationError

from .models import Dog
from config.core.validators.common import (
    DateValidator,
    PhotoValidator,
)


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
        return DateValidator.age_limit(birth_date, 35, "человека")

    def clean_photo(self):
        """Валидация фото"""
        new_photo = self.cleaned_data.get("photo")
        if not new_photo:
            return
        PhotoValidator.photo_size(new_photo)
        PhotoValidator.photo_extension(new_photo)
        PhotoValidator.delete_old_photo(self.instance, "photo", new_photo)
        return new_photo
