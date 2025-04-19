from django.core.management.base import BaseCommand
from django.conf import settings
import subprocess
from pathlib import Path


class Command(BaseCommand):
    help = "Выполняет последовательность деплоя: ccdb, миграции, collectstatic и загрузку данных"

    def add_arguments(self, parser):
        parser.add_argument(
            "--noinput",
            action="store_true",
            help="Пропускать все запросы подтверждения",
        )

    def handle(self, *args, **options):
        fixtures_path = Path(settings.BASE_DIR).parent / "fixtures" / "dogs.json"
        if not fixtures_path.exists():
            self.stderr.write(self.style.ERROR(f"Файл {fixtures_path} не найден!"))
            raise SystemExit(1)
        commands = [
            "ccdb",
            "makemigrations",
            "migrate --noinput" if options["noinput"] else "migrate",
            "ccsu",
            "collectstatic --no-input" if options["noinput"] else "collectstatic",
            f"loaddata {fixtures_path}",
        ]
        for cmd in commands:
            self.stdout.write(self.style.SUCCESS(f">>> Выполняется: {cmd}"))
            try:
                subprocess.run(
                    ["python", "manage.py"] + cmd.split(),
                    check=True,
                    cwd=settings.BASE_DIR,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                )
            except subprocess.CalledProcessError as e:
                self.stderr.write(self.style.ERROR(f'Ошибка в команде "{cmd}": {e}'))
                raise SystemExit(1)
        self.stdout.write(self.style.SUCCESS("Все команды выполнены успешно!"))
