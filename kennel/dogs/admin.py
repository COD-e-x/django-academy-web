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
        "owner",
    )
    list_filter = (
        "breed",
        "birth_date",
        "owner",
    )
    ordering = ("name",)
    search_fields = ("name",)
    readonly_fields = ()
