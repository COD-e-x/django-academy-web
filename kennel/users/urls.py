from django.urls import path

from .apps import UsersConfig
from . import views


app_name = UsersConfig.name


urlpatterns = [
    path("", views.user_login, name="login"),
    path("register/", views.UserRegisterViews.as_view(), name="register"),
    path("profile/", views.user_profile, name="profile"),
    path("profile/update/", views.user_update, name="update"),
    path("profile/password-change/", views.password_change, name="password-change"),
    path("reset-password/", views.reset_password, name="reset-password"),
    path(
        "reset-password-success/",
        views.reset_password_success,
        name="reset-password-success",
    ),
    path("logout/", views.user_logout, name="logout"),
]
