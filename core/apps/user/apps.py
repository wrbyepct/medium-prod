"""Account app."""

from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class AccountConfig(AppConfig):
    """AccountConfig."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "core.apps.user"
    verbose_name = _("user")

    def ready(self):
        from core.apps.user import signals  # noqa: F401
