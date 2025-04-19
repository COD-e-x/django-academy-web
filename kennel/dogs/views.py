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

from config.core.mixins import (
    HtmxRedirectMixin,
    IsOwnerOrAdminRequiredMixin,
)

cache_service = CacheService()


def index(request):
    """
    Отображает главную страницу сайта. (временно, буду переделывать)
    Возвращает шаблон с первыми тремя породами собак.
    """

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
    """
    Отображает список всех пород собак.
    Использует кэширование для оптимизации запросов.
    """

    model = Breed
    template_name = "dogs/breed/list.html"
    extra_context = {"title": "Питомник - Все наши породы"}

    def get_queryset(self):
        return cache_service.get_breeds_cache()


class DogsByBreed(ListView):
    """
    Отображает список собак определенной породы.
    Возвращает сообщение, если собаки данной породы не найдены.
    Использует кэширование для оптимизации запросов.
    """

    model = Dog
    template_name = "dogs/dog/list.html"

    def get_queryset(self):
        return Dog.objects.none()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        dogs, breed = cache_service.get_dogs_by_breed_cache(self.kwargs.get("breed_id"))
        context["object_list"] = dogs
        context["breed"] = breed
        context["title"] = (
            f"Собаки породы - {breed.name}" if dogs else "Собаки этой породы не найдены"
        )
        return context


class DogListView(HtmxRedirectMixin, ListView):
    """
    Отображает список собак с учетом фильтрации по активности.
    Поддерживает HTMX-запросы для динамического обновления контента.
    Разделяет отображение для обычных и HTMX-запросов.
    Использует кэширование для оптимизации запросов.
    """

    model = Dog

    def get_template_names(self):
        if self.request.headers.get("Hx-Request") != "true":
            return ["dogs/dog/list.html"]
        return ["dogs/dog_includes/dog-list-inner.html"]

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.headers.get("Hx-Request") != "true":
            queryset = queryset.filter(is_active=True)
            cache_service.get_dogs_cache()
            return queryset
        active_param = self.request.GET.get("active")
        user_roles = [role.value for role in UserRole]
        if active_param == "1" and self.request.user.role in user_roles:
            queryset = queryset.filter(is_active=True, owner=self.request.user)
        elif active_param == "0" and self.request.user.role in user_roles:
            queryset = queryset.filter(is_active=False, owner=self.request.user)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        active_param = self.request.GET.get("active")
        if active_param == "1":
            context["title"] = "Активные"
        elif active_param == "0":
            context["title"] = "Неактивные"
        else:
            context["title"] = "Все наши собаки"
        return context


class DogCreateView(LoginRequiredMixin, CreateView):
    """
    Создает новую карточку собаки.
    Автоматически устанавливает текущего пользователя как владельца.
    """

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
    """
    Отображает детальную информацию о конкретной собаке.
    """

    model = Dog
    template_name = "dogs/dog/detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        dog = self.object
        context["title"] = f"Вы выбрали: {dog.name}."
        return context


class DogUpdateView(LoginRequiredMixin, IsOwnerOrAdminRequiredMixin, UpdateView):
    """
    Обновляет информацию о собаке.
    Включает обработку формы родителей собаки через formset.
    Доступно только владельцу или администратору.
    """

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
    """
    Удаляет карточку собаки.
    Поддерживает HTMX-запросы для динамического удаления.
    Доступно только владельцу или администратору.
    """

    model = Dog
    template_name = "dogs/dog/detail.html"
    success_url = reverse_lazy("dogs:dogs_list")
    extra_context = {
        "title": "Удалить собаку",
    }


class DogDeleteConfirmView(LoginRequiredMixin, IsOwnerOrAdminRequiredMixin, DetailView):
    """
    Отображает подтверждение удаления собаки.
    Показывает кнопки подтверждения/отмены удаления.
    Доступно только владельцу или администратору.
    """

    model = Dog
    template_name = "dogs/dog_includes/confirm-delete-buttons.html"


class DogDeleteAbort(LoginRequiredMixin, DetailView):
    """
    Отображает стандартные кнопки управления карточкой собаки.
    Используется при отмене удаления.
    """

    model = Dog
    template_name = "dogs/dog_includes/dog-detail-buttons.html"
