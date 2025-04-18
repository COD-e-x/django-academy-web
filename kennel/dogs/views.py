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
from django.forms import inlineformset_factory

from .models import Breed, Dog, DogParent
from .forms import DogForm, DogParentForm
from .services import CacheService
from users.models import UserRole

from config.core.mixins import HtmxRedirectMixin, IsOwnerOrAdminRequiredMixin

cache_service = CacheService()


def index(request):
    """Отображает главную страницу с перечнем первых 3-х пород."""
    context = {
        "object_list": Breed.objects.all()[:3],
        "title": "Питомник - Главная",
    }
    return render(
        request,
        "index.html",
        context,
    )


class BreedList(ListView):
    model = Breed
    template_name = "dogs/breed/list.html"
    extra_context = {"title": "Питомник - Все наши породы"}

    def get_queryset(self):
        return cache_service.get_breeds_cache()


class DogsByBreed(ListView):
    model = Dog
    template_name = "dogs/dog/list.html"

    def get_queryset(self):
        queryset = super().get_queryset().filter(breed_id=self.kwargs.get("breed_id"))
        cache_service.get_dogs_by_breed_cache(self.kwargs.get("breed_id"))
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        dogs, breed = cache_service.get_dogs_by_breed_cache(self.kwargs.get("breed_id"))
        context["object_list"] = dogs
        context["breed"] = breed
        context["title"] = (
            f"Собаки породы - {breed.name}" if dogs else "Собаки этой породы не найдены"
        )
        return context


class DogListView(ListView):
    model = Dog
    template_name = "dogs/dog/list.html"
    extra_context = {
        "title": "Питомник - Все наши собаки",
    }

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(is_active=True)
        cache_service.get_dogs_cache()
        return queryset


class DogDeactivatedListView(LoginRequiredMixin, ListView):
    model = Dog
    template_name = "dogs/dog/list.html"
    extra_context = {
        "title": "Неактивные собаки",
    }

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.user.role in [UserRole.MODERATOR, UserRole.ADMIN]:
            queryset = queryset.filter(is_active=False)
        if self.request.user.role == UserRole.USER:
            queryset = queryset.filter(is_active=False, owner=self.request.user)
        return queryset


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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        DogParentFormset = inlineformset_factory(
            Dog,
            DogParent,
            form=DogParentForm,
            extra=1,
        )
        if self.request.method == "POST":
            formset = DogParentFormset(self.request.POST, instance=self.object)
        else:
            formset = DogParentFormset(instance=self.object)
        context["formset"] = formset
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        formset = context["formset"]
        self.object = form.save()
        if formset.is_valid():
            formset.instance = self.object
            formset.save()
        return super().form_valid(form)


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
