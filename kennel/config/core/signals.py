from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.files.storage import default_storage
from django.core.cache import cache
from dogs.models import Dog, Breed


@receiver(post_delete, sender=Dog)
def delete_photo(sender, instance, **kwargs):
    """Удаление фото при удалении записи."""
    if instance.photo and default_storage.exists(instance.photo.name):
        default_storage.delete(instance.photo.name)


@receiver([post_save, post_delete], sender=Breed)
def clear_breed_cache(sender, **kwargs):
    """Очистка кэша породы при изменении/удалении."""
    cache.delete("breed_list")


@receiver([post_save, post_delete], sender=Dog)
def clear_dog_by_breed_cache(sender, instance, **kwargs):
    """Очистка кэша собак по породе при изменении/удалении."""
    if instance.breed_id:
        cache.delete(f"dogs_by_breed_{instance.breed_id}")


@receiver([post_save, post_delete], sender=Dog)
def clear_dog_list_cache(sender, **kwargs):
    """Очистка кэша собак при изменении/удалении."""
    cache.delete(f"dog_list")
