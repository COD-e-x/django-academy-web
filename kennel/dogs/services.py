from django.core.cache import caches

from .models import (
    Breed,
    Dog,
)


class CacheService:
    """Класс для кэширования данных о собаках и породах."""

    def __init__(self, cache_alias="default", timeout=60 * 60):
        self.cache = caches[cache_alias]
        self.timeout = timeout

    def get_breeds_cache(self):
        """Кэширование списка пород."""
        key = "breed_list"
        breed_list = self.cache.get(key)
        if breed_list is None:
            breed_list = Breed.objects.all()
            self.cache.set(key, breed_list, timeout=self.timeout)
        return breed_list

    def get_dogs_by_breed_cache(self, breed_id: int):
        """Кэширование списка собак по породе."""
        key = f"dogs_by_breed_{breed_id}"
        dogs = self.cache.get(key)
        if dogs is None:
            dogs = Dog.objects.filter(breed_id=breed_id)
            self.cache.set(key, dogs, timeout=self.timeout)
        return dogs

    def get_dogs_cache(self):
        """Кэширование списка собак."""
        key = "dog_list"
        dog_list = self.cache.get(key)
        if dog_list is None:
            dog_list = Dog.objects.all()
            self.cache.set(key, dog_list, timeout=self.timeout)
        return dog_list
