"""Command for creating default super user."""

# ruff: noqa: ARG002, N806, S105
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand


class Commad(BaseCommand):
    """Create default superuser."""

    def handle(self, *args, **options):
        """Create default superuser."""
        User = get_user_model()
        email = "admin@example.com"
        password = "admin"
        first_name = "test"
        last_name = "test"

        if not User.objects.filter(email=email).exists():
            User.objects.create_superuser(
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name,
            )
            self.stdout.write(self.style.SUCCESS("Superuser created."))
        else:
            self.stdout.write(
                self.style.SUCCESS(f"User with this email {email} already exists")
            )
