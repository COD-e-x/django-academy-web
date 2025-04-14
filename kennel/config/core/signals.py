from django.db.models.signals import post_delete
from django.dispatch import receiver
from django.core.files.storage import default_storage
from dogs.models import Dog


@receiver(post_delete, sender=Dog)
def delete_photo(sender, instance, **kwargs):
    """Удаление фото при удалении записи."""
    if instance.photo and default_storage.exists(instance.photo.name):
        default_storage.delete(instance.photo.name)
