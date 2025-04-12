from django.urls import path

from .apps import UsersConfig
from . import views


app_name = UsersConfig.name


urlpatterns = [
    path(
        "",
        views.UserLoginView.as_view(),
        name="login",
    ),
    path(
        "register/",
        views.UserRegisterViews.as_view(),
        name="register",
    ),
    path(
        "profile/",
        views.UserProfileView.as_view(),
        name="profile",
    ),
    path(
        "profile/update/",
        views.UserUpdateView.as_view(),
        name="update",
    ),
    path(
        "profile/password-change/",
        views.UserPasswordChangeView.as_view(),
        name="password-change",
    ),
    path(
        "reset-password/",
        views.reset_password,
        name="reset-password",
    ),
    path(
        "reset-password-success/",
        views.reset_password_success,
        name="reset-password-success",
    ),
    path(
        "logout/",
        views.UserLogoutView.as_view(),
        name="logout",
    ),
]
