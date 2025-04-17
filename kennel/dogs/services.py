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
        """Кэширование списка собак по породу и пароду."""
        dogs_key = f"dogs_by_breed_{breed_id}"
        breed_key = f"breed_{breed_id}"
        dogs = self.cache.get(dogs_key)
        breed = self.cache.get(breed_key)
        if dogs is None or breed is None:
            dogs = Dog.objects.filter(breed=breed_id)
            breed = Breed.objects.get(pk=breed_id)
            self.cache.set(dogs_key, dogs, timeout=self.timeout)
            self.cache.set(breed_key, breed, timeout=self.timeout)
        return dogs, breed

    def get_dogs_cache(self):
        """Кэширование списка собак."""
        key = "dog_list"
        dog_list = self.cache.get(key)
        if dog_list is None:
            dog_list = Dog.objects.all()
            self.cache.set(key, dog_list, timeout=self.timeout)
        return dog_list
