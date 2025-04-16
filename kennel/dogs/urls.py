from django.urls import path

from .apps import DogsConfig
from . import views

app_name = DogsConfig.name

urlpatterns = [
    path(
        "",
        views.index,
        name="index",
    ),
    path(
        "breeds/",
        views.breeds_list,
        name="breeds",
    ),
    path(
        "breeds/<int:breed_id>/dogs/",
        views.dogs_by_breed,
        name="dogs_by_breed",
    ),
    path(
        "dogs/",
        views.DogListView.as_view(),
        name="dogs_list",
    ),
    path(
        "dogs/create/",
        views.DogCreateView.as_view(),
        name="dog_create",
    ),
    path(
        "dogs/detail/<int:pk>/",
        views.DogDetailView.as_view(),
        name="dog_detail",
    ),
    path(
        "dogs/update/<int:pk>/",
        views.DogUpdateView.as_view(),
        name="dog_update",
    ),
    path(
        "dogs/delete/<int:pk>/",
        views.DogDeleteView.as_view(),
        name="dog_delete",
    ),
    path(
        "dogs/delete/confirm/<int:pk>/",
        views.DogDeleteConfirmView.as_view(),
        name="dog_delete_confirm",
    ),
    path(
        "dogs/delete/abort/<int:pk>/",
        views.DogDeleteAbort.as_view(),
        name="dog_delete_abort",
    ),
]
