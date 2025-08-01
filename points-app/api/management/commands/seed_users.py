from django.core.management.base import BaseCommand
from api.models import User


class Command(BaseCommand):
    help = 'usuarios de prueba para la base de datos'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS('Iniciando creación de usuarios...'))

        users_data = [
            {
                "first_name": "Admin",
                "email": "admin@mail.com",
                "is_admin": True,
                "points": 1000,
                "password": "123456"
            },
            {
                "first_name": "User",
                "email": "user@test.com",
                "is_admin": False,
                "points": 500,
                "password": "123456"
            }
        ]

        for user_data in users_data:
            if User.objects.filter(email=user_data['email']).exists():
                self.stdout.write(self.style.WARNING(f"El usuario {user_data['email']} ya existe."))
                continue

            try:
                user = User.objects.create_user(
                    username=user_data['username'],
                    email=user_data['email'],
                    password=user_data['password'],
                    first_name=user_data['first_name'],
                    points=user_data['points'],
                    is_admin=user_data['is_admin'],
                    is_staff=user_data['is_admin'],
                    is_superuser=user_data['is_admin']
                )
                self.stdout.write(self.style.SUCCESS(f"✔ Usuario '{user.email}' creado exitosamente."))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"✖ Error al crear el usuario {user_data['email']}: {e}"))

        self.stdout.write(self.style.SUCCESS('Proceso finalizado.'))