from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class ArticlesConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "core.apps.articles"
    verbose_name = _("Articles")

    def ready(self):
        import core.apps.articles.signals  # noqa: F401
