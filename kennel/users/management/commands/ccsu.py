import os

from django.core.management import BaseCommand

from dotenv import load_dotenv

from users.models import User

load_dotenv()


class Command(BaseCommand):
    def handle(self, *args, **options):
        admin = User.objects.create(
            email=f"{os.getenv("ADMIN_EMAIL")}",
            first_name="Admin",
            last_name="Adminov",
            role="admin",
            is_staff=True,
            is_superuser=True,
            is_active=True,
        )

        admin.set_password(os.getenv("ADMIN_PASS"))
        admin.save()
        print("Admin created")

        moderator = User.objects.create(
            email=f"{os.getenv("MODERATOR_EMAIL")}",
            first_name="Moderator",
            last_name="Moderatorov",
            role="moderator",
            is_staff=True,
            is_superuser=False,
            is_active=True,
        )

        moderator.set_password(os.getenv("MODERATOR_PASS"))
        moderator.save()
        print("Moderator created")

        user = User.objects.create(
            email=f"{os.getenv("USER_EMAIL")}",
            first_name="User",
            last_name="Userov",
            role="user",
            is_staff=False,
            is_superuser=False,
            is_active=True,
        )

        user.set_password(os.getenv("USER_PASS"))
        user.save()
        print("User created")
