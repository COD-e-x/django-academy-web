from django.shortcuts import render, reverse, get_object_or_404
from django.views.generic import (
    ListView,
    CreateView,
    UpdateView,
    DetailView,
    DeleteView,
)
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Breed, Dog
from .forms import DogForm
from config.core.mixins import HtmxRedirectMixin, IsOwnerOrAdminRequiredMixin


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


class DogListView(ListView):
    model = Dog
    template_name = "dogs/dog/list.html"
    extra_context = {
        "title": "Питомник - Все наши собаки",
    }


class DogCreateView(LoginRequiredMixin, CreateView):
    model = Dog
    form_class = DogForm
    template_name = "dogs/dog/create.html"
    success_url = reverse_lazy("dogs:dogs_list")
    extra_context = {
        "title": "Создание карточки собаки",
    }

    # def form_valid(self, form):
    #     self.object = form.save()  # Сохраняет объект в БД
    #     return HttpResponseRedirect(self.get_success_url())

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class DogDetailView(DetailView):
    model = Dog
    template_name = "dogs/dog/detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        dog = self.object
        context["title"] = f"Вы выбрали: {dog.name}."
        return context


class DogUpdateView(LoginRequiredMixin, IsOwnerOrAdminRequiredMixin, UpdateView):
    model = Dog
    form_class = DogForm
    template_name = "dogs/dog/update.html"
    extra_context = {
        "title": "Обновить данные собаки",
    }

    def get_success_url(self):
        return reverse("dogs:dog_detail", kwargs={"pk": self.get_object().pk})


class DogDeleteView(
    LoginRequiredMixin, IsOwnerOrAdminRequiredMixin, HtmxRedirectMixin, DeleteView
):
    model = Dog
    template_name = "dogs/dog/detail.html"
    success_url = reverse_lazy("dogs:dogs_list")
    extra_context = {
        "title": "Удалить собаку",
    }


class DogDeleteConfirmView(LoginRequiredMixin, IsOwnerOrAdminRequiredMixin, DetailView):
    model = Dog
    template_name = "dogs/dog_includes/confirm-delete-buttons.html"


class DogDeleteAbort(LoginRequiredMixin, DetailView):
    model = Dog
    template_name = "dogs/dog_includes/dog-detail-buttons.html"
