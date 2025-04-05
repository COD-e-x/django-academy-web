from django.contrib import admin
from .models import Breed, Dog


@admin.register(Breed)
class BreadAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "description",
    )
    ordering = ("id",)
    search_fields = ("name",)


@admin.register(Dog)
class DogAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "breed",
        "birth_date",
        "photo",
    )
    list_filter = (
        "breed",
        "birth_date",
    )
    ordering = ("name",)
    search_fields = ("name",)
    readonly_fields = ()
