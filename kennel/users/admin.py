from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "role",
        "last_name",
        "first_name",
        "email",
        "phone",
        "telegram",
        "gender",
        "profile_picture",
        "is_active",
        "date_joined",
        "last_login",
    )
    list_display_links = (
        "id",
        "email",
    )
    list_editable = (
        "is_active",
        "phone",
        "telegram",
        "role",
    )
    search_fields = (
        "email",
        "phone",
        "telegram",
    )
    list_filter = (
        "is_active",
        "gender",
        "date_joined",
        "last_login",
    )
    readonly_fields = (
        "date_joined",
        "last_login",
    )
    ordering = ("id",)

    fieldsets = (
        (
            None,
            {
                "fields": (
                    "role",
                    "first_name",
                    "last_name",
                    "email",
                    "phone",
                    "telegram",
                    "birth_date",
                    "gender",
                    "profile_picture",
                    "is_active",
                )
            },
        ),
        (
            _("Permissions"),
            {
                "fields": ("is_staff", "is_superuser", "groups", "user_permissions"),
            },
        ),
        (
            _("Important dates"),
            {
                "fields": ("last_login", "date_joined"),
            },
        ),
        # (
        #     _("Password"),
        #     {
        #         "fields": ("password",),
        #     },
        # ),
    )
