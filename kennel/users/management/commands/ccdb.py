from django.core.management.base import BaseCommand
import psycopg2
import os


class Command(BaseCommand):
    """
    Команда для создания базы данных в PostgreSQL и пользователя из .env
    """

    def handle(self, *args, **options):
        db_name = os.getenv("DB_DATABASE")
        db_user = os.getenv("DB_USER")
        db_password = os.getenv("DB_PASSWORD")
        db_host = os.getenv("DB_HOST")
        db_port = os.getenv("DB_PORT")
        try:
            conn = psycopg2.connect(
                dbname="postgres",
                user=db_user,
                password=db_password,
                host=db_host,
                port=db_port,
            )
            conn.autocommit = True
            cursor = conn.cursor()
            cursor.execute(f"CREATE DATABASE {db_name};")
            self.stdout.write(f"Создана базы дынных '{db_name}'")
            # Настраиваем пользователя с правами доступа к базе с базовыми настройками
            cursor.execute(f"ALTER USER {db_user} WITH PASSWORD '{db_password}';")
            cursor.execute(f"ALTER ROLE {db_user} SET client_encoding TO 'utf8';")
            cursor.execute(
                f"ALTER ROLE {db_user} SET default_transaction_isolation TO 'read committed';"
            )
            cursor.execute(f"ALTER ROLE {db_user} SET timezone TO 'UTC';")
            cursor.execute(f"GRANT ALL PRIVILEGES ON DATABASE {db_name} TO {db_user};")
            self.stdout.write(
                self.style.SUCCESS("Настройка базы данных завершена успешно")
            )
        except psycopg2.Error as e:
            self.stdout.write(self.style.ERROR(f"Database error: {e}"))
        finally:
            if "cursor" in locals():
                cursor.close()
            if "conn" in locals():
                conn.close()
