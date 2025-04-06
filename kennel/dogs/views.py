import os

from django.http import HttpResponse
from django.shortcuts import render, reverse, redirect, get_object_or_404

from .models import Breed, Dog
from .forms import DogForm


def index(request):
    """Отображает главную страницу с перечнем первых 3-х пород."""
    context = {
        "breeds": Breed.objects.all()[:3],
        "title": "Питомник - Главная",
    }
    return render(
        request,
        "index.html",
        context,
    )


def breeds_list(request):
    """Отображает список всех пород собак."""
    context = {
        "breeds": Breed.objects.all(),
        "title": "Питомник - Все наши породы",
    }
    return render(
        request,
        "dogs/breed/list.html",
        context,
    )


def dogs_by_breed(request, pk: int):
    """Отображает список собак для конкретной породы."""
    breed = get_object_or_404(Breed, pk=pk)
    context = {
        "dogs": Dog.objects.filter(breed_id=pk),
        "title": f"Собаки породы - {breed.name}",
        "breed_pk": breed.pk,
    }
    return render(
        request,
        "dogs/dog/list.html",
        context,
    )


def dogs_list(request):
    """Отображает список всех собак в питомнике."""
    context = {
        "dogs": Dog.objects.all(),
        "title": "Питомник - Все наши собаки",
    }
    return render(
        request,
        "dogs/dog/list.html",
        context,
    )


def dog_create(request):
    """Обрабатывает создание новой собаки через форму."""
    form = DogForm(request.POST, request.FILES)
    if request.method == "POST":
        if form.is_valid():
            form.save()
            return redirect("dogs:dogs_list")
    context = {
        "form": form
    }
    return render(
        request,
        "dogs/dog/create.html",
        context,
    )


def dog_detail(request, pk: int):
    """Отображает подробную информацию о собаке."""
    dog_object = get_object_or_404(Dog, pk=pk)
    breed_name = dog_object.breed.name
    context = {
        "dog": dog_object,
        "title": f"Вы выбрали: {dog_object.name}.",
        "breed_name": f"Порода {breed_name}",
    }
    return render(
        request,
        "dogs/dog/detail.html",
        context,
    )


def dog_update(request, pk: int):
    """Обновляет данные у собаки."""
    dog_object = get_object_or_404(Dog, pk=pk)
    if request.method == "POST":
        form = DogForm(request.POST, request.FILES, instance=dog_object)
        if form.is_valid():
            dog_object = form.save()
            dog_object.save()
            return redirect(reverse("dogs:dog_detail", args=[pk]))
    context = {
        "dog": dog_object,
        "form": DogForm(instance=dog_object),
    }
    return render(
        request,
        "dogs/dog/update.html",
        context,
    )


def dog_delete_confirm(request, pk: int):
    """Показывает кнопки подтверждения удаления."""
    dog_object = get_object_or_404(Dog, pk=pk)
    return render(
        request,
        "dogs/dog_includes/confirm-delete-buttons.html",
        {"dog": dog_object},
    )


def dog_delete_abort(request, pk):
    """Отмена удаления собаки."""
    dog_object = get_object_or_404(Dog, pk=pk)
    return render(
        request,
        "dogs/dog_includes/dog-detail-buttons.html",
        {"dog": dog_object},
    )


def dog_delete(request, pk: int):
    """Удаляет собаку."""
    dog_object = get_object_or_404(Dog, pk=pk)
    if request.method == "POST":
        if dog_object.photo:
            file_path = dog_object.photo.path
            if os.path.exists(file_path):
                os.remove(file_path)
        dog_object.delete()
        if "HX-Request" in request.headers:
            response = HttpResponse()
            response["HX-Redirect"] = "/dogs/"
            return response
    context = {
        "dog": dog_object,
    }
    return render(
        request,
        "dogs/dog/detail.html",
        context,
    )
