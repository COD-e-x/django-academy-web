import os

from django.core.management import BaseCommand
from ...models import User

from dotenv import load_dotenv
load_dotenv()

class Command(BaseCommand):
    def handle(self, *args, **options):
        admin_user = User.objects.create(
            email=f"{os.getenv('ADMIN_EMAIL')}",
            first_name="Admin",
            last_name="Adminov",
            is_staff=True,
            is_superuser=True,
            is_active=True,
        )

        admin_user.set_password(os.getenv("ADMIN_PASS"))
        admin_user.save()
